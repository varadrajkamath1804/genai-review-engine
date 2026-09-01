from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.pdf_extraction_service import PDFExtractionService


def get_document_service() -> DocumentService:
    return DocumentService(
        pdf_extraction_service=PDFExtractionService(),
        chunking_service=ChunkingService(),
    )
