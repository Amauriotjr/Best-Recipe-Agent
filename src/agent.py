from src.tools.ingredient_parser import IngredientParserTool
from src.tools.recipe_api import RecipeApiTool
from src.tools.recipe_database import RecipeDatabaseTool
from src.tools.recipe_matcher import RecipeMatcherTool
from src.tools.report_generator import ReportGeneratorTool


class RecipeRecommendationAgent:

    def __init__(self, database_path: str = "data/recipes.json"):
        self.ingredient_parser = IngredientParserTool()
        self.recipe_api = RecipeApiTool()
        self.recipe_database = RecipeDatabaseTool(database_path)
        self.recipe_matcher = RecipeMatcherTool()
        self.report_generator = ReportGeneratorTool()

    def recommend(
        self,
        raw_ingredients: str,
        max_results: int = 5,
        use_online_api: bool = True
    ) -> dict:

        user_ingredients = self.ingredient_parser.parse(raw_ingredients)

        recipes = []
        data_source = "local database"
        fallback_used = False
        api_error = None

        if use_online_api:
            try:
                recipes = self.recipe_api.search_recipes_by_ingredients(
                    user_ingredients=user_ingredients,
                    limit=max(max_results * 3, 10)
                )

                if recipes:
                    data_source = "TheMealDB API"

            except Exception as error:
                fallback_used = True
                api_error = str(error)

        if not recipes:
            recipes = self.recipe_database.load_recipes()
            data_source = "local database"

            if use_online_api:
                fallback_used = True

        recommendations = self.recipe_matcher.match(
            user_ingredients=user_ingredients,
            recipes=recipes,
            max_results=max_results
        )

        return self.report_generator.generate(
            user_ingredients=user_ingredients,
            recommendations=recommendations,
            data_source=data_source,
            fallback_used=fallback_used,
            api_error=api_error
        )