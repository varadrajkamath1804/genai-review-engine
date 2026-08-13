from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.repositories.review_repository import ReviewRepository
from app.repositories.user_repository import UserRepository
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.dependencies.embedding import get_embedding_service
from app.services.embedding_service import EmbeddingService
from app.services.semantic_search_service import SemanticSearchService


def get_review_repository(
    db: AsyncSession = Depends(get_db),
) -> ReviewRepository:
    return ReviewRepository(db)


def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepository:
    return UserRepository(db)


def get_refresh_token_repository(
    db: AsyncSession = Depends(get_db),
) -> RefreshTokenRepository:
    return RefreshTokenRepository(db)


def get_semantic_search_service(
    embedding_service: EmbeddingService = Depends(
        get_embedding_service,
    ),
    review_repository: ReviewRepository = Depends(
        get_review_repository,
    ),
) -> SemanticSearchService:

    return SemanticSearchService(
        embedding_service=embedding_service,
        review_repository=review_repository,
    )
