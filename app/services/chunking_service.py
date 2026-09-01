from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkingService:
    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap=50,
    ):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def chunk_documents(
        self,
        documents: list[Document],
    ) -> list[Document]:
        return self.splitter.split_documents(documents)
