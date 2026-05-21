from src.agent import RecipeRecommendationAgent


def test_agent_returns_recommendations():
    agent = RecipeRecommendationAgent(database_path="data/recipes.json")

    result = agent.recommend("eggs, cheese, salt", max_results=3)

    assert "summary" in result
    assert "recommendations" in result
    assert len(result["recommendations"]) > 0


def test_agent_returns_user_ingredients():
    agent = RecipeRecommendationAgent(database_path="data/recipes.json")

    result = agent.recommend("eggs, cheese", max_results=3)

    assert result["user_ingredients"] == ["eggs", "cheese"]