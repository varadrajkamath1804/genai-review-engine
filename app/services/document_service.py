from pathlib import Path
from fastapi import UploadFile

from app.services.pdf_extraction_service import PDFExtractionService
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService


class DocumentService:

    def __init__(
        self,
        pdf_extraction_service: PDFExtractionService,
        chunking_service: ChunkingService,
        embedding_service: EmbeddingService,
    ):
        self.pdf_extraction_service = pdf_extraction_service
        self.chunking_service = chunking_service
        self.embedding_service = embedding_service

    async def process_upload(
        self,
        file: UploadFile,
    ):
        # Temporary file used by PyPDFLoader.
        temp_path = Path(f"temp_{file.filename}")

        try:
            # Read uploaded PDF.
            contents = await file.read()

            # Write PDF to temporary location.
            temp_path.write_bytes(contents)

            # -------------------------------
            # 1. Extract PDF pages
            # -------------------------------
            documents = await self.pdf_extraction_service.extract(str(temp_path))

            # -------------------------------
            # 2. Split pages into chunks
            # -------------------------------
            chunks = self.chunking_service.chunk_documents(documents)

            # -------------------------------
            # 3. Extract text from chunks
            # -------------------------------
            texts = [chunk.page_content for chunk in chunks]

            # -------------------------------
            # 4. Generate embeddings
            # -------------------------------
            embeddings = await self.embedding_service.generate_embeddings(texts)

            # -------------------------------
            # 5. Combine chunk + embedding
            # -------------------------------
            chunk_data = []

            for chunk, embedding in zip(chunks, embeddings):
                # Validate embedding dimension.
                if len(embedding) != self.embedding_service.dimension:
                    raise ValueError(
                        "Embedding dimension does not match expected dimension"
                    )

                chunk_data.append(
                    {
                        "content": chunk.page_content,
                        "metadataa": chunk.metadata,
                        "embedding": embedding,
                    }
                )

            return chunk_data
        finally:
            if temp_path.exists():
                temp_path.unlink()
