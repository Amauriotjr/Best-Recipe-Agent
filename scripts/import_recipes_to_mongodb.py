import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.tools.ingredient_normalizer import IngredientNormalizer


DEFAULT_INPUT_FILE = Path("data/recipes.json")


def load_recipes(input_file: Path) -> list[dict]:
    if not input_file.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_file}. "
            "Run scripts/import_github_recipes.py first."
        )

    with input_file.open("r", encoding="utf-8") as file:
        recipes = json.load(file)

    if not isinstance(recipes, list):
        raise ValueError("Input JSON must contain a list of recipes.")

    return recipes


def prepare_recipe(recipe: dict, normalizer: IngredientNormalizer) -> dict:
    ingredients = recipe.get("ingredients", [])

    normalized_ingredients = []

    for ingredient in ingredients:
        normalized = normalizer.normalize(ingredient)

        if normalized and normalized not in normalized_ingredients:
            normalized_ingredients.append(normalized)

    recipe["normalized_ingredients"] = normalized_ingredients

    return recipe


def import_to_mongodb(
    input_file: Path,
    clear_collection: bool = False,
    batch_size: int = 1000
) -> None:
    load_dotenv()

    mongodb_uri = os.getenv("MONGODB_URI")
    database_name = os.getenv("MONGODB_DATABASE", "recipe_agent")
    collection_name = os.getenv("MONGODB_COLLECTION", "recipes")

    if not mongodb_uri:
        raise ValueError(
            "MONGODB_URI is not configured. "
            "Create a .env file before importing data."
        )

    recipes = load_recipes(input_file)

    client = MongoClient(mongodb_uri)
    database = client[database_name]
    collection = database[collection_name]

    if clear_collection:
        collection.delete_many({})

    normalizer = IngredientNormalizer()

    total_inserted = 0
    batch = []

    for recipe in recipes:
        prepared_recipe = prepare_recipe(recipe, normalizer)

        if not prepared_recipe.get("normalized_ingredients"):
            continue

        batch.append(prepared_recipe)

        if len(batch) >= batch_size:
            result = collection.insert_many(batch)
            total_inserted += len(result.inserted_ids)
            batch = []

    if batch:
        result = collection.insert_many(batch)
        total_inserted += len(result.inserted_ids)

    collection.create_index("normalized_ingredients")
    collection.create_index("name")

    print(f"Imported {total_inserted} recipes into MongoDB.")
    print(f"Database: {database_name}")
    print(f"Collection: {collection_name}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import converted recipes into MongoDB."
    )

    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT_FILE),
        help="Path to the converted recipes JSON file."
    )

    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear the MongoDB collection before importing."
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="Number of recipes inserted per batch."
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    import_to_mongodb(
        input_file=Path(args.input),
        clear_collection=args.clear,
        batch_size=args.batch_size
    )