from fastapi import Depends
from groq import AsyncGroq
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.groq import get_groq_client
from app.core.config import Settings, get_settings
from app.dependencies.repository import get_semantic_search_service
from app.services.rag_service import RAGService
from app.services.semantic_search_service import SemanticSearchService
from app.dependencies.database import get_db
from app.dependencies.embedding import get_embedding_service
from app.repositories.review_chunk_repository import ReviewChunkRepository
from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService
from app.services.rag_ingestion_service import RAGIngestionService


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


def get_chunking_service() -> ChunkingService:
    # Create the service responsible for splitting
    # LangChain Documents into smaller chunks.
    return ChunkingService()


def get_document_service() -> DocumentService:
    # Create the service responsible for converting
    # Review database objects into LangChain Documents.
    return DocumentService()


def get_review_chunk_repository(
    db: AsyncSession = Depends(get_db),
) -> ReviewChunkRepository:
    # Create the repository using the current
    # asynchronous database session.
    return ReviewChunkRepository(
        db=db,
    )


def get_rag_ingestion_service(
    document_service: DocumentService = Depends(
        get_document_service,
    ),
    chunking_service: ChunkingService = Depends(
        get_chunking_service,
    ),
    embedding_service: EmbeddingService = Depends(
        get_embedding_service,
    ),
    review_chunk_repository: ReviewChunkRepository = Depends(
        get_review_chunk_repository,
    ),
) -> RAGIngestionService:
    # Assemble all services required for the
    # complete RAG ingestion pipeline.
    return RAGIngestionService(
        document_service=document_service,
        chunking_service=chunking_service,
        embedding_service=embedding_service,
        review_chunk_repository=review_chunk_repository,
    )
