import os

from dotenv import load_dotenv
from pymongo import MongoClient

from src.tools.ingredient_normalizer import IngredientNormalizer


class MongoRecipeDatabaseTool:

    def __init__(
        self,
        mongodb_uri: str | None = None,
        database_name: str | None = None,
        collection_name: str | None = None
    ):
        load_dotenv()

        self.mongodb_uri = mongodb_uri or os.getenv("MONGODB_URI")
        self.database_name = database_name or os.getenv(
            "MONGODB_DATABASE",
            "recipe_agent"
        )
        self.collection_name = collection_name or os.getenv(
            "MONGODB_COLLECTION",
            "recipes"
        )

        self.normalizer = IngredientNormalizer()
        self.source_name = "MongoDB recipe database"

    def _get_collection(self):
        if not self.mongodb_uri:
            raise ValueError(
                "MONGODB_URI is not configured. "
                "Create a .env file with your MongoDB connection string."
            )

        client = MongoClient(self.mongodb_uri, serverSelectionTimeoutMS=5000)

        client.admin.command("ping")

        database = client[self.database_name]

        return database[self.collection_name]

    def find_candidate_recipes(
        self,
        user_ingredients: list[str],
        limit: int = 500
    ) -> list[dict]:
        normalized_user_ingredients = [
            self.normalizer.normalize(ingredient)
            for ingredient in user_ingredients
        ]

        collection = self._get_collection()

        cursor = collection.find(
            {
                "normalized_ingredients": {
                    "$in": normalized_user_ingredients
                }
            },
            {
                "_id": 0
            }
        ).limit(limit)

        return list(cursor)

    def get_status(self) -> dict:
        collection = self._get_collection()

        return {
            "status": "connected",
            "database": self.database_name,
            "collection": self.collection_name,
            "total_recipes": collection.count_documents({})
        }