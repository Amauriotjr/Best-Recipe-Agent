from src.agent import RecipeRecommendationAgent


class FakeRecipeDatabaseTool:
    source_name = "fake recipe database"

    def find_candidate_recipes(self, user_ingredients, limit=500):
        return [
            {
                "name": "Simple Pancakes",
                "ingredients": ["flour", "milk", "eggs", "sugar", "butter"],
                "category": "breakfast",
                "difficulty": "easy",
                "source": "test"
            },
            {
                "name": "Peanut Butter Sandwich",
                "ingredients": ["bread", "peanut butter"],
                "category": "snack",
                "difficulty": "easy",
                "source": "test"
            }
        ]


def test_agent_returns_recommendations():
    agent = RecipeRecommendationAgent(
        recipe_database=FakeRecipeDatabaseTool()
    )

    result = agent.recommend(
        raw_ingredients="flour, sugar, eggs, butter",
        max_results=5
    )

    assert "summary" in result
    assert "recommendations" in result
    assert result["data_source"] == "fake recipe database"
    assert len(result["recommendations"]) > 0


def test_agent_returns_user_ingredients():
    agent = RecipeRecommendationAgent(
        recipe_database=FakeRecipeDatabaseTool()
    )

    result = agent.recommend(
        raw_ingredients="flour, sugar",
        max_results=3
    )

    assert result["user_ingredients"] == ["flour", "sugar"]