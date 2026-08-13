from pydantic import BaseModel, Field


class SemanticSearchRequest(BaseModel):

    query: str = Field(
        min_length=11,
        max_length=500,
        description="Natural-language search query",
    )

    limit: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of similar reviews to return",
    )
