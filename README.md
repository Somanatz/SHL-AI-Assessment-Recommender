# SHL AI Assignment - Assessment Recommender

This app recommends relevant SHL assessments for a given job description using sentence embeddings.

## 🔍 Features
- **Input:** Job Description (Text or URL)
- **Output:** Top 10 recommended SHL assessments
- **Tech Stack:** Python, FastAPI (Backend), Streamlit (Frontend), Sentence Transformers

---

## 🚀 How to Run the App Locally

### 1. Backend (FastAPI)

```bash
uvicorn main:app --reload       # Run backend
streamlit run app.py   # Run frontend
