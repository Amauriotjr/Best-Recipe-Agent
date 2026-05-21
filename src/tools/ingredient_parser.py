class IngredientParserTool:

    def parse(self, raw_ingredients: str) -> list[str]:
        if raw_ingredients is None or not raw_ingredients.strip():
            raise ValueError("Ingredient list cannot be empty.")

        ingredients = [
            ingredient.strip().lower()
            for ingredient in raw_ingredients.split(",")
            if ingredient.strip()
        ]

        if not ingredients:
            raise ValueError("No valid ingredients were provided.")

        unique_ingredients = []

        for ingredient in ingredients:
            if ingredient not in unique_ingredients:
                unique_ingredients.append(ingredient)

        return unique_ingredients