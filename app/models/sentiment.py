from pydantic import BaseModel, Field


class SentimentResponse(BaseModel):
    """
    Represents the AI sentiment analysis response.
    """

    sentiment: str = Field(description="Predicted sentiment")
    confidence: float = Field(
        ge=0, le=1, description="Confidence score between 0.0 and 1.0"
    )
