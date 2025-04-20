# frontend/app.py
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import streamlit as st
from recommend import load_catalog, recommend_assessments
from utils import extract_text

st.title("SHL AI Assessment Recommender")

query = st.text_area("Enter Job Description or URL")

if st.button("Recommend"):
    if query:
        text = extract_text(query)
        df, embeddings = load_catalog()
        results = recommend_assessments(text, df, embeddings)

        for _, row in results.iterrows():
            st.markdown(f"**URL:** [{row['url']}]({row['url']})")
            st.markdown(f"**Adaptive Support:** {row['adaptive_support']}")
            st.markdown(f"**Description:** {row['description']}")
            st.markdown(f"**Duration:** {row['duration']}")
            st.markdown(f"**Remote Support:** {row['remote_support']}")
            st.markdown(f"**Test Types:** {row['test_types']}")
            st.markdown("---")
    else:
        st.error("Please enter a job description or URL.")