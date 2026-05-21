import requests


class RecipeApiTool:
    
    BASE_URL = "https://www.themealdb.com/api/json/v1/1"

    def search_by_main_ingredient(self, ingredient: str) -> list[dict]:
        normalized_ingredient = ingredient.strip().lower().replace(" ", "_")

        response = requests.get(
            f"{self.BASE_URL}/filter.php",
            params={"i": normalized_ingredient},
            timeout=8
        )

        response.raise_for_status()

        data = response.json()

        return data.get("meals") or []

    def get_recipe_details(self, meal_id: str) -> dict | None:
        response = requests.get(
            f"{self.BASE_URL}/lookup.php",
            params={"i": meal_id},
            timeout=8
        )

        response.raise_for_status()

        data = response.json()
        meals = data.get("meals") or []

        if not meals:
            return None

        return meals[0]

    def search_recipes_by_ingredients(
        self,
        user_ingredients: list[str],
        limit: int = 10
    ) -> list[dict]:
        if not user_ingredients:
            raise ValueError("At least one ingredient is required.")

        main_ingredient = user_ingredients[0]

        meal_summaries = self.search_by_main_ingredient(main_ingredient)

        recipes = []

        for meal in meal_summaries[:limit]:
            meal_id = meal.get("idMeal")

            if not meal_id:
                continue

            details = self.get_recipe_details(meal_id)

            if details:
                recipes.append(self._convert_api_recipe(details))

        return recipes

    def _convert_api_recipe(self, api_recipe: dict) -> dict:
        ingredients = []
        ingredient_measures = []

        for index in range(1, 21):
            ingredient = api_recipe.get(f"strIngredient{index}")
            measure = api_recipe.get(f"strMeasure{index}")

            if ingredient and ingredient.strip():
                clean_ingredient = ingredient.strip().lower()
                clean_measure = measure.strip() if measure else ""

                ingredients.append(clean_ingredient)

                ingredient_measures.append(
                    {
                        "ingredient": clean_ingredient,
                        "measure": clean_measure
                    }
                )

        return {
            "id": api_recipe.get("idMeal"),
            "name": api_recipe.get("strMeal", "Unknown Recipe"),
            "ingredients": ingredients,
            "ingredient_measures": ingredient_measures,
            "category": api_recipe.get("strCategory", "unknown"),
            "area": api_recipe.get("strArea", "unknown"),
            "difficulty": "unknown",
            "instructions": api_recipe.get("strInstructions", ""),
            "image_url": api_recipe.get("strMealThumb"),
            "source_url": api_recipe.get("strSource"),
            "youtube_url": api_recipe.get("strYoutube"),
            "source": "TheMealDB API"
        }