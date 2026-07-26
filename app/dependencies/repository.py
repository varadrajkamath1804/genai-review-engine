from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.repositories.review_repository import ReviewRepository
from app.repositories.user_repository import UserRepository


def get_review_repository(
    db: AsyncSession = Depends(get_db),
) -> ReviewRepository:
    return ReviewRepository(db)


def get_user_repository(
    db=Depends(get_db),
) -> UserRepository:
    return UserRepository(db)
