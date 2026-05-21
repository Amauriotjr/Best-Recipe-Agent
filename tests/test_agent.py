from src.agent import RecipeRecommendationAgent


def test_agent_returns_recommendations_using_local_database():
    agent = RecipeRecommendationAgent(database_path="data/recipes.json")

    result = agent.recommend(
        raw_ingredients="flour, sugar, eggs, butter",
        max_results=5,
        use_online_api=False
    )

    assert "summary" in result
    assert "recommendations" in result
    assert result["data_source"] == "local database"
    assert len(result["recommendations"]) > 0


def test_agent_returns_user_ingredients():
    agent = RecipeRecommendationAgent(database_path="data/recipes.json")

    result = agent.recommend(
        raw_ingredients="flour, sugar",
        max_results=3,
        use_online_api=False
    )

    assert result["user_ingredients"] == ["flour", "sugar"]