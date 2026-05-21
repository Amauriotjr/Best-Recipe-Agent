from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    ingredients: str = Field(
        example="flour, sugar, eggs, butter"
    )
    max_results: int = Field(
        default=5,
        ge=1,
        le=20,
        example=5
    )
    use_online_api: bool = Field(
        default=True,
        example=False
    )