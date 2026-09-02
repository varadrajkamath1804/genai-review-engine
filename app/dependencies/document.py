from fastapi import Request

from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.pdf_extraction_service import PDFExtractionService
from app.services.embedding_service import EmbeddingService


def get_document_service(request: Request) -> DocumentService:
    return DocumentService(
        pdf_extraction_service=PDFExtractionService(),
        chunking_service=ChunkingService(),
        embedding_service=request.app.state.embedding,
    )
