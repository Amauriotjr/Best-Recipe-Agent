from fastapi import FastAPI, HTTPException, Query

from src.agent import RecipeRecommendationAgent
from src.schemas import RecommendationRequest


app = FastAPI(
    title="AI Recipe Recommendation Agent",
    description=(
        "An agent-based Python API that recommends recipes based on "
        "available ingredients using MongoDB as the recipe database."
    ),
    version="0.4.0"
)

agent = RecipeRecommendationAgent()


@app.get("/")
def root():
    return {
        "message": "Welcome to the AI Recipe Recommendation Agent API.",
        "version": "0.4.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/database/status")
def database_status():
    try:
        return agent.recipe_database.get_status()

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/recommend")
def recommend_recipes(request: RecommendationRequest):
    try:
        return agent.recommend(
            raw_ingredients=request.ingredients,
            max_results=request.max_results
        )

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.get("/recipes/search")
def search_recipes(
    ingredients: str = Query(
        example="flour, sugar, eggs"
    ),
    limit: int = Query(default=10, ge=1, le=100)
):
    try:
        parsed_ingredients = agent.ingredient_parser.parse(ingredients)

        recipes = agent.recipe_database.find_candidate_recipes(
            user_ingredients=parsed_ingredients,
            limit=limit
        )

        return {
            "data_source": agent.recipe_database.source_name,
            "ingredients": parsed_ingredients,
            "total_results": len(recipes),
            "recipes": recipes
        }

    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))