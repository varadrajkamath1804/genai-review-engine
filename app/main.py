from fastapi import FastAPI, Depends

from app.models.review import ReviewInput
from app.models.sentiment import SentimentResponse
from app.services.ai_service import AIService
from app.dependencies.ai import get_ai_service

app = FastAPI()


@app.post("/analyze")
async def analyze_review(
    review: ReviewInput, ai_service: AIService = Depends(get_ai_service)
) -> SentimentResponse:

    return await ai_service.analyze_review(review)
