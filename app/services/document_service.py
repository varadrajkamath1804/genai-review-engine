from langchain_core.documents import Document
from app.db.models.review import Review


class DocumentService:

    def review_to_document(
        self,
        review: Review,
    ) -> Document:
        """
        Convert a Review database object into a LangChain Document.

        The review text becomes page_content.

        Database fields that help identify, filter, or provide context
        become metadata.

        The embedding is intentionally not included because embeddings
        are generated later for the chunk content.
        """
        return Document(
            page_content=review.review,
            metadata={
                "review_id": review.id,
                "sentiment": review.sentiment,
                "confidence": review.confidence,
            },
        )

    def reviews_to_document(self, reviews: list[Review]) -> list[Document]:
        """
        Convert multiple Review objects into LangChain Documents.
        """
        return [self.review_to_document(review) for review in reviews]
