from src.tools.ingredient_normalizer import IngredientNormalizer


class RecipeMatcherTool:

    def __init__(self):
        self.normalizer = IngredientNormalizer()

    def match(
        self,
        user_ingredients: list[str],
        recipes: list[dict],
        max_results: int = 5
    ) -> list[dict]:

        normalized_user_ingredients = {
            self.normalizer.normalize(ingredient)
            for ingredient in user_ingredients
            if ingredient and str(ingredient).strip()
        }

        recommendations = []

        for recipe in recipes:
            recipe_ingredients = recipe.get("ingredients", [])

            if not recipe_ingredients:
                continue

            available_ingredients = []
            missing_ingredients = []

            for recipe_ingredient in recipe_ingredients:
                normalized_recipe_ingredient = self.normalizer.normalize(
                    recipe_ingredient
                )

                if not normalized_recipe_ingredient:
                    continue

                if normalized_recipe_ingredient in normalized_user_ingredients:
                    available_ingredients.append(str(recipe_ingredient))
                else:
                    missing_ingredients.append(str(recipe_ingredient))

            total_valid_ingredients = (
                len(available_ingredients) + len(missing_ingredients)
            )

            if total_valid_ingredients == 0:
                continue

            match_score = round(
                (len(available_ingredients) / total_valid_ingredients) * 100,
                2
            )

            if match_score > 0:
                recommendations.append(
                    {
                        "id": recipe.get("id"),
                        "name": recipe.get("name", "Unknown Recipe"),
                        "category": recipe.get("category", "unknown"),
                        "area": recipe.get("area", "unknown"),
                        "difficulty": recipe.get("difficulty", "unknown"),
                        "source": recipe.get("source", "MongoDB"),
                        "match_score": match_score,
                        "available_ingredients": sorted(available_ingredients),
                        "missing_ingredients": sorted(missing_ingredients),
                        "original_ingredients": recipe.get("original_ingredients"),
                        "instructions": self._format_instructions(
                            recipe.get("instructions", [])
                        ),
                        "source_url": recipe.get("source_url"),
                    }
                )

        recommendations.sort(
            key=lambda recipe: recipe["match_score"],
            reverse=True
        )

        return recommendations[:max_results]

    def _format_instructions(self, instructions):
        
        if instructions is None:
            return []

        if isinstance(instructions, list):
            return [
                str(step).strip()
                for step in instructions
                if str(step).strip()
            ]

        if isinstance(instructions, str):
            cleaned_text = instructions.strip()

            if not cleaned_text:
                return []

            return [cleaned_text]

        return [str(instructions)]