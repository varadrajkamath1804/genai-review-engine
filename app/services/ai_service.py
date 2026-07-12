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
        prompt = f"""Analyze the following customer review.

        Return:
        - sentiment
        - confidence

        Review:
        {review.review}
        """

        try:
            pass
            # response = await self.client.responses.create(
            #     model="gpt-4.1-mini",
            #     input=prompt,
            # )

            # Parse the AI response here.

        except Exception as error:
            raise RuntimeError("Failed to analyze review") from error

        mock_response = {"sentiment": "Positive", "confidence": 0.99}

        return SentimentResponse(
            sentiment=mock_response["sentiment"], confidence=mock_response["confidence"]
        )
