from src.tools.ingredient_parser import IngredientParserTool
from src.tools.recipe_matcher import RecipeMatcherTool
from src.tools.recipe_mongodb import MongoRecipeDatabaseTool
from src.tools.report_generator import ReportGeneratorTool


class RecipeRecommendationAgent:

    def __init__(self, recipe_database=None):
        self.ingredient_parser = IngredientParserTool()
        self.recipe_database = recipe_database or MongoRecipeDatabaseTool()
        self.recipe_matcher = RecipeMatcherTool()
        self.report_generator = ReportGeneratorTool()

    def recommend(
        self,
        raw_ingredients: str,
        max_results: int = 5
    ) -> dict:

        user_ingredients = self.ingredient_parser.parse(raw_ingredients)

        candidate_recipes = self.recipe_database.find_candidate_recipes(
            user_ingredients=user_ingredients,
            limit=max(max_results * 100, 500)
        )

        recommendations = self.recipe_matcher.match(
            user_ingredients=user_ingredients,
            recipes=candidate_recipes,
            max_results=max_results
        )

        return self.report_generator.generate(
            user_ingredients=user_ingredients,
            recommendations=recommendations,
            data_source=self.recipe_database.source_name
        )