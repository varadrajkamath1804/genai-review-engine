from pydantic import BaseModel


class IngestionResponse(BaseModel):
    review_id: int
    chunks_created: int
