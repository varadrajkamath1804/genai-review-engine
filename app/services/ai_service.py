import asyncio
from openai import AsyncOpenAI

from app.models.review import ReviewInput
from app.models.sentiment import SentimentResponse


class AIService:
    """
    Service responsible for AI-powered review analysis.
    """

    def __init__(self, client: AsyncOpenAI):
        self.client = client

    async def analyze_review(self, review: ReviewInput) -> SentimentResponse:
        await asyncio.sleep(2)
        return SentimentResponse(sentiment="Positive", confidence=0.99)
