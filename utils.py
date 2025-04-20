# utils.py
import requests
from bs4 import BeautifulSoup

# utils.py
def extract_text(input_data: str) -> str:
    if input_data.startswith("http"):
        try:
            response = requests.get(input_data)
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            return ' '.join(p.get_text() for p in paragraphs)
        except Exception as e:
            raise ValueError(f"Failed to extract text from URL: {e}")
    return input_data.strip()

