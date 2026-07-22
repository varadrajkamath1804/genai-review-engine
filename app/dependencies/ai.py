from fastapi import Depends
from groq import AsyncGroq

from app.core.config import Settings, get_settings
from app.clients.groq import get_groq_client
from app.dependencies.repository import get_review_repository
from app.services.ai_service import AIService
from app.repositories.review_repository import ReviewRepository


def get_ai_service(
    client: AsyncGroq = Depends(get_groq_client),
    settings: Settings = Depends(get_settings),
    review_repository: ReviewRepository = Depends(get_review_repository),
) -> AIService:
    return AIService(client, settings, review_repository)
