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
from app.services.embedding_service import EmbeddingService

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
        embedding_service: EmbeddingService,
    ):
        self.client = client
        self.settings = settings
        self.review_repository = review_repository
        self.cache_service = cache_service
        self.embedding_service = embedding_service

    async def analyze_review(
        self,
        review: ReviewInput,
    ) -> SentimentResponse:

        # Create a deterministic Redis key from the review text.
        # The same review can therefore reuse its cached sentiment result.
        cache_key = review_sentiment_key(review.review)

        # This lock prevents multiple requests from simultaneously

        lock_key = f"lock:{cache_key}"

        # Check Redis before making an expensive Groq request.
        cached = await self.cache_service.get(cache_key)

        if cached:
            logger.info("Cache hit for review")

            # Convert the cached JSON data back into our Pydantic response model.
            validated_response = SentimentResponse.model_validate(cached)

            # Sentiment came from cache, but this is still a new database
            # record, so we must generate its embedding for semantic search.
            embedding = await self.embedding_service.generate_embedding(
                review.review,
            )

            # Build the database entity containing both the AI result
            # and the 384-dimensional embedding.
            review_entity = Review(
                review=review.review,
                sentiment=validated_response.sentiment,
                confidence=validated_response.confidence,
                embedding=embedding,
            )

            await self.review_repository.save(review_entity)

            return validated_response

        logger.info("Cache miss for review")

        # This prevents duplicate LLM requests when multiple clients
        # Check whether already this review is being checked using groq - if yes return lock value to check later

        lock_value = await self.cache_service.acquire_lock(lock_key)

        # If lock is set from this request then returns the lock_value - if lock is already set then returns None
        if lock_value is None:

            logger.info("Another request is processing this review")

            # Another request already owns the lock.
            # Instead of immediately failing, wait briefly for that
            # request to finish and populate the Redis cache.
            for _ in range(10):
                await asyncio.sleep(0.1)

                cached = await self.cache_service.get(cache_key)

                if cached:
                    validated_response = SentimentResponse.model_validate(cached)
                    return validated_response

            # The other request did not populate the cache in time.
            # Try to acquire the lock ourselves.
            lock_value = await self.cache_service.acquire_lock(lock_key)

            if lock_value is None:
                raise CacheLockException()

        try:

            # Check Redis one more time after acquiring the lock.
            #
            # Another request may have completed between our first
            # cache check and acquiring the lock.
            cached = await self.cache_service.get(cache_key)

            if cached:

                logger.info("Cache populated before Groq call")

                validated_response = SentimentResponse.model_validate(cached)

                return validated_response

            # Prompt used to make Groq return only the structured
            # sentiment information required by the application.
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

            # Send the review to Groq for sentiment analysis.
            response = await self.client.chat.completions.create(
                model=self.settings.GROQ_MODEL,
                messages=messages,
                temperature=0,
            )

            # Extract the model's response and convert the JSON string
            # into a Python dictionary.
            content = response.choices[0].message.content
            parsed_response = json.loads(content)

            # Validate the LLM output against our Pydantic model.
            validated_response = SentimentResponse.model_validate(parsed_response)

            # Store the sentiment result in Redis so future identical
            # requests can avoid another Groq API call. Cache Population
            await self.cache_service.set(
                cache_key,
                parsed_response,
            )

            # Generate the semantic representation of the review.
            #
            # The embedding service returns a 384-dimensional vector
            # that will be stored in PostgreSQL using pgvector.
            embedding = await self.embedding_service.generate_embedding(
                review.review,
            )

            # Create the database entity containing the original review,
            # sentiment result, confidence score, and embedding.
            review_entity = Review(
                review=review.review,
                sentiment=validated_response.sentiment,
                confidence=validated_response.confidence,
                embedding=embedding,
            )

            # Repository is responsible only for persisting the entity.
            await self.review_repository.save(review_entity)

            return validated_response

        finally:

            # Always release the distributed lock, even if Groq,
            # embedding generation, or database persistence fails.
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

        # Repository handles database querying and pagination.
        reviews = await self.review_repository.get_all(
            page,
            size,
            sentiment,
            review,
            sort_by,
            sort_order,
        )

        # Convert SQLAlchemy entities into API response models.
        return [ReviewResponse.model_validate(review) for review in reviews]

    async def get_review(
        self,
        review_id: int,
    ) -> ReviewResponse:

        # Fetch the requested review from the repository.
        review = await self.review_repository.get_by_id(review_id)

        # Convert a missing database record into our application exception.
        if review is None:
            raise ReviewNotFoundException(review_id)

        # Return a validated API response instead of exposing
        # the database entity directly.
        return ReviewResponse.model_validate(review)

    async def update_review(
        self,
        review_id: int,
        review: UpdateReview,
    ) -> ReviewResponse:

        # Retrieve the existing database entity before updating it.
        existing_review = await self.review_repository.get_by_id(review_id)

        if existing_review is None:
            raise ReviewNotFoundException(review_id)

        # Keep the old text because the old Redis cache key
        # is based on the previous review text.
        old_review_text = existing_review.review

        # Recalculate sentiment because the review text changed.
        validated_response = await self._analyze_sentiment(
            review.review,
        )

        # The text changed, so its embedding must also be regenerated.
        # Keeping the old embedding would make semantic search incorrect.
        embedding = await self.embedding_service.generate_embedding(
            review.review,
        )

        # Update all values derived from the new review text.
        existing_review.review = review.review
        existing_review.sentiment = validated_response.sentiment
        existing_review.confidence = validated_response.confidence
        existing_review.embedding = embedding

        # Persist the modified entity.
        updated_review = await self.review_repository.update(
            existing_review,
        )

        # Remove the cache entry associated with the old review text.
        await self.invalidate_cache(old_review_text)

        return ReviewResponse.model_validate(updated_review)

    async def _analyze_sentiment(
        self,
        review: str,
    ) -> SentimentResponse:

        # Build the prompt used when an existing review is updated.
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

        # Ask Groq to analyze the updated review.
        response = await self.client.chat.completions.create(
            model=self.settings.GROQ_MODEL,
            messages=messages,
            temperature=0,
        )

        # Parse and validate the LLM response.
        content = response.choices[0].message.content
        parsed_response = json.loads(content)

        return SentimentResponse.model_validate(parsed_response)

    async def delete_review(
        self,
        review_id: int,
    ) -> None:

        # Fetch the review before deleting it so we can obtain
        # the review text required to invalidate its Redis cache.
        review = await self.review_repository.get_by_id(review_id)

        if review is None:
            raise ReviewNotFoundException(review_id)

        review_text = review.review

        # Delete the database record.
        # Its embedding is automatically removed because it belongs
        # to the same Review row.
        await self.review_repository.delete(review)

        # Remove the cached sentiment associated with the deleted review.
        await self.invalidate_cache(review_text)

    async def invalidate_cache(
        self,
        review_text: str,
    ) -> None:

        # Recreate the Redis key from the review text and invalidate it.
        cache_key = review_sentiment_key(review_text)

        await self.cache_service.invalidate(cache_key)
