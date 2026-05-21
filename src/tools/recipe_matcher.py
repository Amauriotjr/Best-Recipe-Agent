import re


class RecipeMatcherTool:

    def match(
        self,
        user_ingredients: list[str],
        recipes: list[dict],
        max_results: int = 5
    ) -> list[dict]:

        normalized_user_ingredients = {
            self._normalize_ingredient(ingredient)
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
                normalized_recipe_ingredient = self._normalize_ingredient(
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
                        "source": recipe.get("source", "local database"),
                        "match_score": match_score,
                        "available_ingredients": sorted(available_ingredients),
                        "missing_ingredients": sorted(missing_ingredients),
                        "original_ingredients": recipe.get("original_ingredients"),
                        "image_url": recipe.get("image_url"),
                        "source_url": recipe.get("source_url"),
                        "youtube_url": recipe.get("youtube_url"),
                    }
                )

        recommendations.sort(
            key=lambda recipe: recipe["match_score"],
            reverse=True
        )

        return recommendations[:max_results]

    def _normalize_ingredient(self, ingredient: str) -> str:

        ingredient = str(ingredient).lower().strip()

        ingredient = ingredient.replace("-", " ")

        ingredient = re.sub(r"[^a-z0-9\s]", " ", ingredient)

        ingredient = re.sub(r"\s+", " ", ingredient)

        ingredient = ingredient.strip()

        ingredient = self._singularize_phrase(ingredient)

        return ingredient

    def _singularize_phrase(self, ingredient: str) -> str:

        words = ingredient.split()

        singular_words = [
            self._singularize_word(word)
            for word in words
        ]

        return " ".join(singular_words)

    def _singularize_word(self, word: str) -> str:
        if len(word) > 4 and word.endswith("ies"):
            return word[:-3] + "y"

        if len(word) > 4 and word.endswith("oes"):
            return word[:-2]

        if len(word) > 4 and word.endswith("ches"):
            return word[:-2]

        if len(word) > 4 and word.endswith("shes"):
            return word[:-2]

        if len(word) > 4 and word.endswith("xes"):
            return word[:-2]

        if len(word) > 3 and word.endswith("s"):
            return word[:-1]

        return word