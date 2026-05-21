from fastapi import FastAPI, HTTPException, Query

from src.agent import RecipeRecommendationAgent
from src.schemas import RecommendationRequest


app = FastAPI(
    title="AI Recipe Recommendation Agent",
    description=(
        "An agent-based Python API that recommends recipes based on "
        "available ingredients using TheMealDB API and a local fallback database."
    ),
    version="0.3.0"
)

agent = RecipeRecommendationAgent()


@app.get("/")
def root():
    return {
        "message": "Welcome to the AI Recipe Recommendation Agent API.",
        "version": "0.3.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/recommend")
def recommend_recipes(request: RecommendationRequest):
    try:
        return agent.recommend(
            raw_ingredients=request.ingredients,
            max_results=request.max_results,
            use_online_api=request.use_online_api
        )

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except FileNotFoundError as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.get("/recipes/local")
def get_local_recipes(limit: int = Query(default=20, ge=1, le=100)):
    try:
        recipes = agent.recipe_database.load_recipes()

        return {
            "source": "local database",
            "total_recipes": len(recipes),
            "recipes": recipes[:limit]
        }

    except FileNotFoundError as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.get("/external/search/{ingredient}")
def search_external_recipes(
    ingredient: str,
    limit: int = Query(default=5, ge=1, le=10)
):
    try:
        meal_summaries = agent.recipe_api.search_by_main_ingredient(ingredient)

        return {
            "source": "TheMealDB API",
            "main_ingredient": ingredient,
            "results": meal_summaries[:limit]
        }

    except Exception as error:
        raise HTTPException(status_code=502, detail=str(error))