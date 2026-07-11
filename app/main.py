from fastapi import FastAPI

from app.models.review import ReviewInput
from app.models.sentiment import SentimentResponse
from app.services.ai_service import AIService

app = FastAPI()


@app.post("/analyze")
async def analyze_review(review: ReviewInput) -> SentimentResponse:
    ai_service = AIService()

    return await ai_service.analyze_review(review)
