# main.py
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from pydantic import BaseModel
from recommend import load_catalog, recommend_assessments
from utils import extract_text
import numpy as np

app = FastAPI()

df, embeddings = load_catalog()

# Input model with only one 'query'
class RecommendationRequest(BaseModel):
    query: str

@app.get("/health")
def health_check():
    return JSONResponse(
        content={"status": "success", "message": "OK"},
        status_code=status.HTTP_200_OK
    )

@app.post("/recommend")
def get_recommendations(payload: RecommendationRequest):
    if not payload.query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query is required."
        )

    try:
        # Decide if query is a URL or plain text
        if payload.query.strip().lower().startswith("http"):
            input_text = extract_text(payload.query)
        else:
            input_text = payload.query

        results = recommend_assessments(input_text, df, embeddings)
        
        results = results.replace([np.nan, np.inf, -np.inf], None)

        response_data = results[[
            'url', 'adaptive_support', 'description', 'duration',
            'remote_support', 'test_types'
        ]].to_dict(orient="records")

        return JSONResponse(
            content={"recommended_assessments": response_data},
            status_code=status.HTTP_200_OK
        )

    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": f"Failed to process input: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
