from pydantic import BaseModel


class RAGSource(BaseModel):
    id: int
    review: str


class RAGResponse(BaseModel):
    answer: str
    sources: list[RAGSource]
