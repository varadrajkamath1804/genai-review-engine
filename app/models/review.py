from pydantic import BaseModel, Field


class ReviewInput(BaseModel):
    id: int = Field(
        gt=0, 
        description="Unique review identifier"
    )

    review:str = Field(
        min_length=1,
        max_length=5000,
        description="Customer Review Sheet"
    )