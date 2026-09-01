from pathlib import Path
from fastapi import UploadFile

from app.services.pdf_extraction_service import PDFExtractionService
from app.services.chunking_service import ChunkingService


class DocumentService:

    def __init__(
        self,
        pdf_extraction_service: PDFExtractionService,
        chunking_service: ChunkingService,
    ):
        self.pdf_extraction_service = pdf_extraction_service
        self.chunking_service = chunking_service

    async def process_upload(
        self,
        file: UploadFile,
    ):
        temp_path = Path(f"temp_{file.filename}")

        try:
            contents = await file.read()
            temp_path.write_bytes(contents)
            documents = await self.pdf_extraction_service.extract(str(temp_path))
            chunks = self.chunking_service.chunk_documents(documents)
            return chunks
        finally:
            if temp_path.exists():
                temp_path.unlink()
