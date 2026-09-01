from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


class PDFExtractionService:

    async def extract(
        self,
        file_path: str,
    ) -> list[Document]:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return documents
