from src.tools.ingredient_parser import IngredientParserTool
from src.tools.recipe_database import RecipeDatabaseTool
from src.tools.recipe_matcher import RecipeMatcherTool
from src.tools.report_generator import ReportGeneratorTool


class RecipeRecommendationAgent:

    def __init__(self, database_path: str = "data/recipes.json"):
        self.ingredient_parser = IngredientParserTool()
        self.recipe_database = RecipeDatabaseTool(database_path)
        self.recipe_matcher = RecipeMatcherTool()
        self.report_generator = ReportGeneratorTool()

    def recommend(self, raw_ingredients: str, max_results: int = 5) -> dict:
        user_ingredients = self.ingredient_parser.parse(raw_ingredients)

        recipes = self.recipe_database.load_recipes()

        recommendations = self.recipe_matcher.match(
            user_ingredients=user_ingredients,
            recipes=recipes,
            max_results=max_results
        )

        report = self.report_generator.generate(
            user_ingredients=user_ingredients,
            recommendations=recommendations
        )

        return report