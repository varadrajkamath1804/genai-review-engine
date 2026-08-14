from fastapi import Depends
from groq import AsyncGroq

from app.clients.groq import get_groq_client
from app.core.config import Settings, get_settings
from app.dependencies.repository import get_semantic_search_service
from app.services.rag_service import RAGService
from app.services.semantic_search_service import SemanticSearchService


def get_rag_service(
    client: AsyncGroq = Depends(get_groq_client),
    settings: Settings = Depends(get_settings),
    semantic_search_service: SemanticSearchService = Depends(
        get_semantic_search_service
    ),
) -> RAGService:
    return RAGService(
        client=client,
        settings=settings,
        semantic_search_service=semantic_search_service,
    )
