from app.db.models.review import Review
from app.db.models.review_chunk import ReviewChunk
from app.repositories.review_chunk_repository import ReviewChunkRepository
from app.services.chunking_service import ChunkingService
from app.services.document_service import DocumentService
from app.services.embedding_service import EmbeddingService


class RAGIngestionService:

    def __init__(
        self,
        document_service: DocumentService,
        chunking_service: ChunkingService,
        embedding_service: EmbeddingService,
        review_chunk_repository: ReviewChunkRepository,
    ):
        # Service responsible for converting a Review
        # into a LangChain Document.
        self.document_service = document_service

        # Service responsible for splitting Documents
        # into smaller chunks.
        self.chunking_service = chunking_service

        # Service responsible for generating vector embeddings.
        self.embedding_service = embedding_service

        # Repository responsible for saving ReviewChunk
        # objects into PostgreSQL.
        self.review_chunk_repository = review_chunk_repository

    async def ingest_review(
        self,
        review: Review,
    ) -> list[ReviewChunk]:

        # STEP 1:
        # Convert the database Review object into
        # a LangChain Document.
        document = self.document_service.review_to_document(
            review=review,
        )

        # STEP 2:
        # Split the LangChain Document into smaller
        # LangChain Document chunks.
        chunk_documents = self.chunking_service.chunk_documents(
            documents=[document],
        )

        saved_chunks = []

        # STEP 3:
        # Process every generated chunk.
        for chunk_index, chunk_document in enumerate(
            chunk_documents,
        ):

            # STEP 4:
            # Generate an embedding specifically for
            # this chunk's text.
            embedding = await self.embedding_service.generate_embedding(
                text=chunk_document.page_content,
            )

            # STEP 5:
            # Create the database model representing
            # this individual chunk.
            review_chunk = ReviewChunk(
                review_id=review.id,
                content=chunk_document.page_content,
                chunk_index=chunk_index,
                embedding=embedding,
                # Preserve metadata created when the
                # original Review was converted into
                # a LangChain Document.
                metadata_=chunk_document.metadata,
            )

            # STEP 6:
            # Save the chunk and its embedding.
            saved_chunk = await self.review_chunk_repository.save(
                review_chunk=review_chunk,
            )

            saved_chunks.append(saved_chunk)

        return saved_chunks
