from app.db.models.review import Review
from app.repositories.review_repository import ReviewRepository
from app.services.embedding_service import EmbeddingService
from app.core.config import Settings


class SemanticSearchService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
        review_repository: ReviewRepository,
        settings: Settings,
    ):
        self.embedding_service = embedding_service
        self.review_repository = review_repository
        self.settings = settings

    async def semantic_search(
        self,
        query: str,
        limit: int = 5,
    ) -> list[Review]:

        query_embedding = await self.embedding_service.generate_embedding(
            query,
        )

        reviews = await self.review_repository.semantic_search(
            query_embedding=query_embedding,
            limit=limit,
            max_distance=self.settings.RAG_SIMILARITY_THRESHOLD,
        )

        return reviews
