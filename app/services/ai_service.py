import asyncio
from app.models.review import ReviewInput
from app.models.sentiment import SentimentResponse


class AIService:
    """
    Service responsible for AI-powered review analysis.
    """

    async def analyze_review(self, review: ReviewInput) -> SentimentResponse:
        await asyncio.sleep(2)
        return SentimentResponse(sentiment="Positive", confidence=0.99)
