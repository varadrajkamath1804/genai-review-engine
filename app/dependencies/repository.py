from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.database import get_db
from app.repositories.review_repository import ReviewRepository


def get_review_repository(db: AsyncSession = Depends(get_db)) -> ReviewRepository:
    return ReviewRepository(db)
