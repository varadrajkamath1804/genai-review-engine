from groq import AsyncGroq
import json
import logging

from app.exceptions.review import ReviewNotFoundException
from app.db.models.review import Review
from app.models.review.query import SortField, SortOrder
from app.core.config import Settings
from app.models.review.review import ReviewInput
from app.models.review.update_review import UpdateReview
from app.models.review.review_response import ReviewResponse
from app.models.review.sentiment import SentimentResponse
from app.repositories.review_repository import ReviewRepository

logger = logging.getLogger(__name__)


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

    async def analyze_review(
        self,
        review: ReviewInput,
    ) -> SentimentResponse:
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

        response = await self.client.chat.completions.create(
            model=self.settings.GROQ_MODEL,
            messages=messages,
            temperature=0,
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

    async def get_all_reviews(
        self,
        page: int,
        size: int,
        sentiment: str | None,
        review: str | None,
        sort_by: SortField,
        sort_order: SortOrder,
    ) -> list[ReviewResponse]:
        reviews = await self.review_repository.get_all(
            page,
            size,
            sentiment,
            review,
            sort_by,
            sort_order,
        )
        return [ReviewResponse.model_validate(review) for review in reviews]

    async def get_review(
        self,
        review_id: int,
    ) -> ReviewResponse:
        review = await self.review_repository.get_by_id(review_id)
        if review is None:
            raise ReviewNotFoundException(
                review_id,
            )
        return ReviewResponse.model_validate(
            review,
        )

    async def update_review(
        self,
        review_id: int,
        review: UpdateReview,
    ) -> ReviewResponse:
        existing_review = await self.review_repository.get_by_id(review_id)
        if existing_review is None:
            raise ReviewNotFoundException(review_id)
        validated_response = await self._analyze_sentiment(review.review)
        existing_review.review = review.review
        existing_review.sentiment = validated_response.sentiment
        existing_review.confidence = validated_response.confidence
        updated_review = await self.review_repository.update(existing_review)
        return ReviewResponse.model_validate(updated_review)

    async def _analyze_sentiment(
        self,
        review: str,
    ) -> SentimentResponse:
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
                "content": review,
            },
        ]
        response = await self.client.chat.completions.create(
            model=self.settings.GROQ_MODEL,
            messages=messages,
            temperature=0,
        )

        content = response.choices[0].message.content
        parsed_response = json.loads(content)
        return SentimentResponse.model_validate(parsed_response)

    async def delete_review(
        self,
        review_id: int,
    ) -> None:

        review = await self.review_repository.get_by_id(review_id)
        if review is None:
            raise ReviewNotFoundException(review_id)
        await self.review_repository.delete(review)
