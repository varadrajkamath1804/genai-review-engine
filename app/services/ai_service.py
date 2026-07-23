from groq import AsyncGroq
import json
from fastapi import HTTPException

from app.core.config import Settings
from app.models.review import ReviewInput
from app.models.review_response import ReviewResponse
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

    async def get_all_reviews(self) -> list[ReviewResponse]:
        try:
            reviews = await self.review_repository.get_all()
            return [ReviewResponse.model_validate(review) for review in reviews]
        except Exception as error:
            raise RuntimeError("Failed to Get Reviews") from error

    async def get_review(self, review_id) -> ReviewResponse:
        try:
            review = await self.review_repository.get_by_id(review_id)
            if review is None:
                raise HTTPException(status_code=404, detail="Review not found")
            return ReviewResponse.model_validate(review)
        except HTTPException:
            raise
        except Exception as error:
            raise RuntimeError("Failed to Get Review") from error
