from groq import AsyncGroq
import json
import logging
import asyncio

from app.exceptions.review import ReviewNotFoundException
from app.exceptions.cache import CacheLockException
from app.db.models.review import Review
from app.models.review.query import SortField, SortOrder
from app.core.config import Settings
from app.models.review.review import ReviewInput
from app.models.review.update_review import UpdateReview
from app.models.review.review_response import ReviewResponse
from app.models.review.sentiment import SentimentResponse
from app.repositories.review_repository import ReviewRepository
from app.services.cache_service import CacheService
from app.core.cache_keys import review_sentiment_key

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
        cache_service: CacheService,
    ):
        self.client = client
        self.settings = settings
        self.review_repository = review_repository
        self.cache_service = cache_service

    async def analyze_review(
        self,
        review: ReviewInput,
    ) -> SentimentResponse:

        cache_key = review_sentiment_key(review.review)
        lock_key = f"lock:{cache_key}"
        cached = await self.cache_service.get(cache_key)

        if cached:
            logger.info("Cache hit for review")

            validated_response = SentimentResponse.model_validate(cached)
            review_entity = Review(
                review=review.review,
                sentiment=validated_response.sentiment,
                confidence=validated_response.confidence,
            )

            await self.review_repository.save(review_entity)
            return validated_response

        logger.info("Cache miss for review")

        lock_value = await self.cache_service.acquire_lock(lock_key)

        if lock_value is None:

            logger.info("Another request is processing this review")

            for _ in range(10):
                await asyncio.sleep(0.1)
                cached = await self.cache_service.get(cache_key)
                if cached:
                    validated_response = SentimentResponse.model_validate(cached)
                    return validated_response

            lock_value = await self.cache_service.acquire_lock(lock_key)
            if lock_value is None:
                raise CacheLockException()

        try:

            cached = await self.cache_service.get(cache_key)
            if cached:

                logger.info("Cache populated before Groq call")

                validated_response = SentimentResponse.model_validate(cached)

                return validated_response

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

            await self.cache_service.set(
                cache_key,
                parsed_response,
            )

            review_entity = Review(
                review=review.review,
                sentiment=validated_response.sentiment,
                confidence=validated_response.confidence,
            )

            await self.review_repository.save(review_entity)
            return validated_response
        finally:

            await self.cache_service.release_lock(
                lock_key,
                lock_value,
            )

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

        old_review_text = existing_review.review

        validated_response = await self._analyze_sentiment(
            review.review,
        )
        existing_review.review = review.review
        existing_review.sentiment = validated_response.sentiment
        existing_review.confidence = validated_response.confidence

        updated_review = await self.review_repository.update(
            existing_review,
        )

        await self.invalidate_cache(old_review_text)

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

        review_text = review.review

        await self.review_repository.delete(review)
        await self.invalidate_cache(review_text)

    async def invalidate_cache(
        self,
        review_text: str,
    ) -> None:
        cache_key = review_sentiment_key(review_text)

        await self.cache_service.invalidate(cache_key)
