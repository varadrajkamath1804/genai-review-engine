from app.services.embedding_service import EmbeddingService


def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()
