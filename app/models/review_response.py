from pydantic import BaseModel, ConfigDict


class ReviewResponse(BaseModel):
    id: int
    review: str
    sentiment: str
    confidence: float

    model_config = ConfigDict(from_attributes=True)
