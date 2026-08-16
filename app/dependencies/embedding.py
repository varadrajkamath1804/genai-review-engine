from fastapi import Request
from app.services.embedding_service import EmbeddingService


def get_embedding_service(request: Request) -> EmbeddingService:
    return request.app.state.embedding
