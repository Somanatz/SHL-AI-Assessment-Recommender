# recommend.py
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

# Load and embed the catalog
def load_catalog(path='Web_Scrap_Scr\shl_product_catalog_combined.csv'):
    df = pd.read_csv(path)
    catalog_texts = df['title'].fillna('') + " " + df['test_types'].fillna('') + " " + df['description'].fillna('')
    embeddings = model.encode(catalog_texts.tolist(), show_progress_bar=True)
    return df, embeddings

# Recommend assessments
def recommend_assessments(query_text, df, embeddings, top_n=10):
    query_embedding = model.encode([query_text])
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = np.argsort(similarities)[::-1][:top_n]
    top_results = df.iloc[top_indices].copy()
    top_results['similarity'] = similarities[top_indices]
    return top_results