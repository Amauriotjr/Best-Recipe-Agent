from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    ingredients: str = Field(
        example="eggs, cheese, tomato"
    )
    max_results: int = Field(
        default=5,
        ge=1,
        le=10,
        example=3
    )