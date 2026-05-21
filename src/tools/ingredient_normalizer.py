import re


class IngredientNormalizer:

    def normalize(self, ingredient: str) -> str:
        ingredient = str(ingredient).lower().strip()

        ingredient = ingredient.replace("-", " ")

        ingredient = re.sub(r"[^a-z0-9\s]", " ", ingredient)

        ingredient = re.sub(r"\s+", " ", ingredient)

        ingredient = ingredient.strip()

        return self._singularize_phrase(ingredient)

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