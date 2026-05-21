from fastapi import FastAPI, HTTPException

from src.agent import RecipeRecommendationAgent
from src.schemas import RecommendationRequest


app = FastAPI(
    title="AI Recipe Recommendation Agent",
    description="An agent-based Python API that recommends recipes based on available ingredients.",
    version="0.1.0"
)

agent = RecipeRecommendationAgent()


@app.get("/")
def root():
    return {
        "message": "Welcome to the AI Recipe Recommendation Agent API."
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/recommend")
def recommend_recipes(request: RecommendationRequest):
    try:
        result = agent.recommend(
            raw_ingredients=request.ingredients,
            max_results=request.max_results
        )

        return result

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except FileNotFoundError as error:
        raise HTTPException(status_code=500, detail=str(error))