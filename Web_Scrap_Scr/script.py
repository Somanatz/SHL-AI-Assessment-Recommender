import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Category map for skill types
category_map = {
    'A': 'Ability & Aptitude',
    'B': 'Biodata & Situational Judgement',
    'C': 'Competencies',
    'D': 'Development & 360',
    'E': 'Assessment Exercises',
    'K': 'Knowledge & Skills',
    'P': 'Personality & Behavior',
    'S': 'Simulations'
}

def extract_test_categories(td_tag, category_map):
    spans = td_tag.find_all('span', class_='product-catalogue__key')
    category_codes = [span.text.strip() for span in spans]
    return [category_map.get(code, code) for code in category_codes]

def is_feature_supported(td_tag):
    return "Yes" if td_tag.find('span', class_='catalogue__circle -yes') else "No"

def extract_description_and_duration(soup):
    description = ''
    duration = ''
    for div in soup.find_all('div', class_='product-catalogue-training-calendar__row'):
        heading = div.find('h4')
        if not heading:
            continue
        heading_text = heading.get_text(strip=True).lower()
        content_tag = div.find('p')
        if 'assessment length' in heading_text and content_tag:
            duration = content_tag.get_text(strip=True).replace("Approximate Completion Time in minutes = ", "")
        elif 'description' in heading_text and content_tag:
            description = content_tag.get_text(strip=True)
    return description, duration

def scrape_shl_table(table_type: int, attr: str):
    if table_type not in [1, 2]:
        raise ValueError("table_type must be either 1 or 2")

    pages = 32 if table_type == 1 else 12
    base_url = "https://www.shl.com/solutions/products/product-catalog/?start={}&type={}&type={}"

    data = []

    for page in range(pages):
        start = page * 12
        url = base_url.format(start, table_type, table_type)
        print(f"🔄 Processing page {page + 1}/{pages}: {url}")

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.find_all('tr', attrs={attr: True})

        for row in rows:
            try:
                title = row.find('td', class_='custom__table-heading__title').get_text(strip=True)
                tds = row.find_all('td')
                product_url = 'https://www.shl.com' + row.find('a')['href']

                prod_response = requests.get(product_url)
                prod_soup = BeautifulSoup(prod_response.content, 'html.parser')
                description, duration = extract_description_and_duration(prod_soup)

                remote_testing = is_feature_supported(tds[1])
                adaptive_irt = is_feature_supported(tds[2])
                test_categories = extract_test_categories(tds[3], category_map)

                data.append({
                    'title': title,
                    'url': product_url,
                    'adaptive_support': adaptive_irt,
                    'description': description,
                    'duration': duration,
                    'remote_support': remote_testing,
                    'test_types': test_categories,
                })

                print(f"✅ Scraped: {title}")
                time.sleep(1)  # Optional: be polite to server
            except Exception as e:
                print(f"❌ Error processing row: {e}")
                continue
    
    # Save results   
    df = pd.DataFrame(data)
    output_filename = f"shl_product_catalog_type{table_type}.csv"
    df.to_csv(output_filename, index=False)
    print(f"📁 Saved: {output_filename}")
    return df
    
def merge_tables(df1, df2):
    print("🔗 Merging both tables...")
    combined_df = pd.concat([df1, df2], ignore_index=True)
    combined_df = combined_df.sort_values("title").reset_index(drop=True)
    combined_df.to_csv("shl_product_catalog_combined.csv", index=False)
    print("✅ Final combined CSV saved as: shl_product_catalog_combined.csv")

# Example usage:
# scrape_shl_table(1)  # For type=1 table
# scrape_shl_table(2)  # For type=2 table

# If you want to run both in sequence:
if __name__ == "__main__":
    print("\nStarting table 1 (type=1)...\n")
    df_type1 = scrape_shl_table(1, "data-entity-id")
    print("\nStarting table 2 (type=2)...\n")
    df_type2 = scrape_shl_table(2, "data-course-id")
    merge_tables(df_type1, df_type2)
    
    