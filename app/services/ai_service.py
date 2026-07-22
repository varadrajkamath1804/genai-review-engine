from groq import AsyncGroq
import json

from app.core.config import Settings
from app.models.review import ReviewInput
from app.db.models.review import Review
from app.models.sentiment import SentimentResponse
from app.repositories.review_repository import ReviewRepository


class AIService:
    """
    Service responsible for AI-powered review analysis.
    """

    def __init__(
        self,
        client: AsyncGroq,
        settings: Settings,
        review_repository: ReviewRepository,
    ):
        self.client = client
        self.settings = settings
        self.review_repository = review_repository

    async def analyze_review(self, review: ReviewInput) -> SentimentResponse:
        messages = [
            {
                "role": "system",
                "content": (
                    """You are a sentiment analysis service.

                    The user's message contains a customer review.
                    Return ONLY a JSON object in this format:

                {
                  "sentiment": "Positive",
                  "confidence": 0.98
                }

                Do not include markdown.
                Do not include explanations.
                Do not include additional text."""
                ),
            },
            {
                "role": "user",
                "content": review.review,
            },
        ]
        try:
            response = await self.client.chat.completions.create(
                model=self.settings.GROQ_MODEL, messages=messages, temperature=0
            )

            content = response.choices[0].message.content
            parsed_response = json.loads(content)

            validated_response = SentimentResponse.model_validate(parsed_response)

            review_entity = Review(
                review=review.review,
                sentiment=validated_response.sentiment,
                confidence=validated_response.confidence,
            )

            await self.review_repository.save(review_entity)
            return validated_response

        except Exception as error:
            raise RuntimeError("Failed to analyze review") from error
