import json
from pathlib import Path


class RecipeDatabaseTool:
    
    def __init__(self, database_path: str = "data/recipes.json"):
        self.database_path = Path(database_path)

    def load_recipes(self) -> list[dict]:
        if not self.database_path.exists():
            raise FileNotFoundError("Recipe database file was not found.")

        with self.database_path.open("r", encoding="utf-8") as file:
            recipes = json.load(file)

        if not isinstance(recipes, list):
            raise ValueError("Recipe database must contain a list of recipes.")

        return recipes