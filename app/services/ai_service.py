import asyncio
from openai import AsyncOpenAI

from app.models.review import ReviewInput
from app.models.sentiment import SentimentResponse


class AIService:
    """
    Service responsible for AI-powered review analysis.
    """

    def __init__(self, client: AsyncOpenAI, model: str):
        self.client = client
        self.model = model

    async def analyze_review(self, review: ReviewInput) -> SentimentResponse:
        prompt = f"""Analyze the following customer review.

        Return:
        - sentiment
        - confidence

        Review:
        {review.review}
        """

        # response = await self.client.responses.create(
        #     model="gpt-4.1-mini",
        #     input=prompt,
        # )

        # Parse the AI response here.

        return SentimentResponse(sentiment="Positive", confidence=0.99)
