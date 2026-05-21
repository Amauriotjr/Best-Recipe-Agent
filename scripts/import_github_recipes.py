import argparse
import json
import re
from pathlib import Path
from typing import Any


DEFAULT_SOURCE_DIR = Path("data/external/recipes-github/index")
DEFAULT_OUTPUT_FILE = Path("data/recipes.json")
DEFAULT_SUMMARY_FILE = Path("data/recipes_import_summary.json")


UNICODE_FRACTIONS = {
    "¼": "1/4",
    "½": "1/2",
    "¾": "3/4",
    "⅐": "1/7",
    "⅑": "1/9",
    "⅒": "1/10",
    "⅓": "1/3",
    "⅔": "2/3",
    "⅕": "1/5",
    "⅖": "2/5",
    "⅗": "3/5",
    "⅘": "4/5",
    "⅙": "1/6",
    "⅚": "5/6",
    "⅛": "1/8",
    "⅜": "3/8",
    "⅝": "5/8",
    "⅞": "7/8",
}


UNITS = {
    "cup", "cups", "c", "tablespoon", "tablespoons", "tbsp", "tbsps",
    "teaspoon", "teaspoons", "tsp", "tsps", "ounce", "ounces", "oz",
    "pound", "pounds", "lb", "lbs", "gram", "grams", "g", "kg",
    "kilogram", "kilograms", "ml", "milliliter", "milliliters",
    "liter", "liters", "l", "pinch", "pinches", "dash", "dashes",
    "can", "cans", "package", "packages", "pkg", "pkgs", "box", "boxes",
    "jar", "jars", "bottle", "bottles", "container", "containers",
    "slice", "slices", "clove", "cloves", "stalk", "stalks",
    "sprig", "sprigs", "bunch", "bunches", "head", "heads",
    "piece", "pieces", "quart", "quarts", "pint", "pints",
}


LEADING_DESCRIPTORS = {
    "a", "an", "about", "approximately", "around",
    "small", "medium", "large", "extra-large", "extra", "jumbo",
    "fresh", "frozen", "canned", "dried", "dry",
    "warm", "hot", "cold", "very",
    "chopped", "diced", "sliced", "minced", "crushed", "grated",
    "shredded", "peeled", "seeded", "drained", "rinsed",
    "softened", "melted", "beaten", "cooked", "uncooked",
    "prepared", "divided", "packed", "sifted",
}


TRAILING_PHRASES = [
    "to taste",
    "as needed",
    "or more to taste",
    "or to taste",
    "for garnish",
]


def normalize_unicode_fractions(text: str) -> str:
    for unicode_fraction, ascii_fraction in UNICODE_FRACTIONS.items():
        text = text.replace(unicode_fraction, f" {ascii_fraction} ")
    return text


def remove_parentheses(text: str) -> str:
    return re.sub(r"\([^)]*\)", " ", text)


def remove_leading_quantities(text: str) -> str:

    quantity_words = (
        "one|two|three|four|five|six|seven|eight|nine|ten|"
        "eleven|twelve|half"
    )

    patterns = [
        r"^\s*\d+\s+\d+/\d+\s+",
        r"^\s*\d+/\d+\s+",
        r"^\s*\d+(\.\d+)?\s+",
        rf"^\s*({quantity_words})\s+",
    ]

    changed = True

    while changed:
        changed = False

        for pattern in patterns:
            new_text = re.sub(pattern, "", text, flags=re.IGNORECASE)

            if new_text != text:
                text = new_text
                changed = True

    return text.strip()


def remove_leading_units_and_descriptors(text: str) -> str:
    words = text.split()

    while words:
        first_word = words[0].strip(".,;:-")

        if first_word in UNITS or first_word in LEADING_DESCRIPTORS:
            words.pop(0)
        else:
            break

    return " ".join(words).strip()


def clean_punctuation(text: str) -> str:
    text = text.replace("–", "-").replace("—", "-")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("’", "'")

    text = re.sub(r"\s+", " ", text)
    text = text.strip(" ,.;:-")

    return text.strip()


def remove_trailing_phrases(text: str) -> str:
    for phrase in TRAILING_PHRASES:
        text = re.sub(
            rf"\b{re.escape(phrase)}\b",
            "",
            text,
            flags=re.IGNORECASE,
        )

    return text.strip()


def clean_ingredient_name(ingredient: str) -> str:

    if not ingredient:
        return ""

    original = ingredient

    ingredient = ingredient.lower().strip()
    ingredient = normalize_unicode_fractions(ingredient)
    ingredient = remove_parentheses(ingredient)

    # Remove preparation details after comma.
    # Example: "walnuts, chopped" -> "walnuts"
    ingredient = ingredient.split(",")[0]

    ingredient = clean_punctuation(ingredient)
    ingredient = remove_trailing_phrases(ingredient)

    ingredient = remove_leading_quantities(ingredient)
    ingredient = remove_leading_units_and_descriptors(ingredient)

    # Some ingredients still start with measurement words after quantity removal.
    ingredient = remove_leading_quantities(ingredient)
    ingredient = remove_leading_units_and_descriptors(ingredient)

    ingredient = clean_punctuation(ingredient)

    if not ingredient:
        return original.lower().strip()

    return ingredient


def convert_recipe(raw_recipe: dict[str, Any]) -> dict[str, Any]:
    raw_ingredients = raw_recipe.get("ingredients", [])

    if not isinstance(raw_ingredients, list):
        raw_ingredients = []

    cleaned_ingredients = []

    for ingredient in raw_ingredients:
        cleaned = clean_ingredient_name(str(ingredient))

        if cleaned and cleaned not in cleaned_ingredients:
            cleaned_ingredients.append(cleaned)

    return {
        "name": raw_recipe.get("title", "Unknown Recipe"),
        "ingredients": cleaned_ingredients,
        "original_ingredients": raw_ingredients,
        "category": "external",
        "difficulty": "unknown",
        "source": raw_recipe.get("source", "dpapathanasiou/recipes"),
        "source_url": raw_recipe.get("url"),
        "tags": raw_recipe.get("tags", []),
        "instructions": raw_recipe.get("directions", []),
        "language": raw_recipe.get("language", "unknown"),
    }


def import_recipes(
    source_dir: Path = DEFAULT_SOURCE_DIR,
    output_file: Path = DEFAULT_OUTPUT_FILE,
    summary_file: Path = DEFAULT_SUMMARY_FILE,
    limit: int | None = None,
) -> None:
    if not source_dir.exists():
        raise FileNotFoundError(
            f"Source directory not found: {source_dir}. "
            "Clone the external repository first."
        )

    recipes = []
    skipped_files = []
    duplicate_keys = set()

    json_files = sorted(source_dir.rglob("*.json"))

    for index, file_path in enumerate(json_files, start=1):
        if index % 1000 == 0:
           print(f"Processing file {index}/{len(json_files)}...")
    
        if limit is not None and len(recipes) >= limit:
            break

        try:
            with file_path.open("r", encoding="utf-8") as file:
                raw_recipe = json.load(file)

            converted_recipe = convert_recipe(raw_recipe)

            recipe_key = (
                converted_recipe["name"].lower().strip(),
                tuple(converted_recipe["ingredients"]),
            )

            if not converted_recipe["ingredients"]:
                skipped_files.append(
                    {
                        "file": str(file_path),
                        "reason": "No valid ingredients found",
                    }
                )
                continue

            if recipe_key in duplicate_keys:
                skipped_files.append(
                    {
                        "file": str(file_path),
                        "reason": "Duplicate recipe",
                    }
                )
                continue

            duplicate_keys.add(recipe_key)
            recipes.append(converted_recipe)

        except Exception as error:
            skipped_files.append(
                {
                    "file": str(file_path),
                    "reason": str(error),
                }
            )

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(recipes, file, indent=2, ensure_ascii=False)

    summary = {
        "source_dir": str(source_dir),
        "output_file": str(output_file),
        "total_json_files_found": len(json_files),
        "total_recipes_imported": len(recipes),
        "total_files_skipped": len(skipped_files),
        "skipped_files_sample": skipped_files[:20],
        "limit_used": limit,
    }

    with summary_file.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2, ensure_ascii=False)

    print(f"Found {len(json_files)} JSON files.")
    print(f"Imported {len(recipes)} recipes into {output_file}.")
    print(f"Skipped {len(skipped_files)} files.")
    print(f"Summary saved to {summary_file}.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import and convert recipes from dpapathanasiou/recipes."
    )

    parser.add_argument(
        "--source",
        default=str(DEFAULT_SOURCE_DIR),
        help="Path to the source recipe index folder.",
    )

    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_FILE),
        help="Path to the output recipes.json file.",
    )

    parser.add_argument(
        "--summary",
        default=str(DEFAULT_SUMMARY_FILE),
        help="Path to the import summary JSON file.",
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional limit for testing. By default, all recipes are imported.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    import_recipes(
        source_dir=Path(args.source),
        output_file=Path(args.output),
        summary_file=Path(args.summary),
        limit=args.limit,
    )