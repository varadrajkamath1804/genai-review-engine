from pydantic import BaseModel


class ReviewAnalysis(BaseModel):
    review_id: int
    review: str
    sentiment: str
    confidence: str
