from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class ChunkingService:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ):
        # LangChain handles the recursive splitting logic internally.
        # Instead of using only one separator, Recursive chunking tries multiple separators.
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def chunk_text(
        self,
        text: str,
    ) -> list[str]:
        # Split plain text and return a list of strings.
        return self.text_splitter.split_text(text)

    def chunk_documents(self, documents: list[Document]) -> list[Document]:
        # Split LangChain Documents into smaller Documents.
        #
        # Each resulting chunk keeps the metadata from
        # its original source Document.
        return self.text_splitter.split_documents(documents)

    def create_chunk_documents(
        self,
        texts: list[str],
        metadatas: list[dict] | None = None,
    ) -> list[Document]:
        # Create chunked LangChain Documents directly from plain text.
        #
        # When metadatas are provided, the metadata at each index
        # belongs to the text at the same index.
        return self.text_splitter.create_documents(
            texts=texts,
            metadatas=metadatas,
        )
