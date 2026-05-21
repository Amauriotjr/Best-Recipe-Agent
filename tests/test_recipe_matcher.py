from src.tools.recipe_matcher import RecipeMatcherTool


def test_recipe_matcher_calculates_score():
    matcher = RecipeMatcherTool()

    user_ingredients = ["eggs", "cheese", "salt"]

    recipes = [
        {
            "name": "Cheese Omelette",
            "ingredients": ["eggs", "cheese", "salt", "pepper"],
            "category": "breakfast",
            "difficulty": "easy"
        }
    ]

    result = matcher.match(user_ingredients, recipes, max_results=1)

    assert len(result) == 1
    assert result[0]["match_score"] == 75.0
    assert result[0]["missing_ingredients"] == ["pepper"]


def test_recipe_matcher_returns_best_recipe_first():
    matcher = RecipeMatcherTool()

    user_ingredients = ["eggs", "cheese", "salt"]

    recipes = [
        {
            "name": "Recipe A",
            "ingredients": ["rice", "onion"]
        },
        {
            "name": "Recipe B",
            "ingredients": ["eggs", "cheese", "salt", "pepper"]
        }
    ]

    result = matcher.match(user_ingredients, recipes, max_results=2)

    assert result[0]["name"] == "Recipe B"


def test_flour_does_not_match_special_flours():
    matcher = RecipeMatcherTool()

    user_ingredients = ["flour"]

    recipes = [
        {
            "name": "Gluten Free Flour Blend",
            "ingredients": [
                "arrowroot flour",
                "brown rice flour",
                "corn flour",
                "sorghum flour",
                "white rice flour",
                "xanthan gum"
            ]
        }
    ]

    result = matcher.match(user_ingredients, recipes, max_results=1)

    assert result == []


def test_flour_does_not_match_flour_tortilla():
    matcher = RecipeMatcherTool()

    user_ingredients = ["flour"]

    recipes = [
        {
            "name": "Peanut Butter Roll",
            "ingredients": [
                "flour tortilla",
                "peanut butter",
                "banana"
            ]
        }
    ]

    result = matcher.match(user_ingredients, recipes, max_results=1)

    assert result == []


def test_peanut_butter_does_not_match_butter():
    matcher = RecipeMatcherTool()

    user_ingredients = ["peanut butter"]

    recipes = [
        {
            "name": "Butter Cookies",
            "ingredients": [
                "butter",
                "flour",
                "sugar"
            ]
        }
    ]

    result = matcher.match(user_ingredients, recipes, max_results=1)

    assert result == []


def test_peanut_butter_matches_only_peanut_butter():
    matcher = RecipeMatcherTool()

    user_ingredients = ["peanut butter"]

    recipes = [
        {
            "name": "Peanut Butter Snack",
            "ingredients": [
                "peanut butter",
                "bread"
            ]
        }
    ]

    result = matcher.match(user_ingredients, recipes, max_results=1)

    assert len(result) == 1
    assert result[0]["available_ingredients"] == ["peanut butter"]
    assert result[0]["missing_ingredients"] == ["bread"]


def test_plural_and_singular_ingredients_match():
    matcher = RecipeMatcherTool()

    user_ingredients = ["eggs", "tomatoes"]

    recipes = [
        {
            "name": "Simple Breakfast",
            "ingredients": [
                "egg",
                "tomato",
                "salt"
            ]
        }
    ]

    result = matcher.match(user_ingredients, recipes, max_results=1)

    assert len(result) == 1
    assert result[0]["available_ingredients"] == ["egg", "tomato"]
    assert result[0]["missing_ingredients"] == ["salt"]


def test_hyphen_variation_matches_same_ingredient():
    matcher = RecipeMatcherTool()

    user_ingredients = ["all purpose flour"]

    recipes = [
        {
            "name": "Cake",
            "ingredients": [
                "all-purpose flour",
                "sugar"
            ]
        }
    ]

    result = matcher.match(user_ingredients, recipes, max_results=1)

    assert len(result) == 1
    assert result[0]["available_ingredients"] == ["all-purpose flour"]
    assert result[0]["missing_ingredients"] == ["sugar"]