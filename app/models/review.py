from pydantic import BaseModel, Field


class ReviewInput(BaseModel):
    """
    Represents one validated review.
    """

    review: str = Field(
        min_length=1, max_length=5000, description="Customer Review Sheet"
    )
