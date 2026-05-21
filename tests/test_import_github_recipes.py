from scripts.import_github_recipes import clean_ingredient_name, convert_recipe


def test_clean_ingredient_removes_ascii_fraction():
    result = clean_ingredient_name("1/2 all-purpose flour")

    assert result == "all-purpose flour"


def test_clean_ingredient_removes_unicode_fraction():
    result = clean_ingredient_name("½ teaspoon salt")

    assert result == "salt"


def test_clean_ingredient_removes_three_quarter_quantity():
    result = clean_ingredient_name("3/4 cup very warm water")

    assert result == "water"


def test_clean_ingredient_removes_measurement_unit():
    result = clean_ingredient_name("3 tablespoons olive oil")

    assert result == "olive oil"


def test_convert_recipe_uses_internal_format():
    raw_recipe = {
        "title": "Test Recipe",
        "ingredients": [
            "1/2 cup flour",
            "½ teaspoon salt",
            "3 tablespoons olive oil"
        ],
        "directions": ["Mix everything."],
        "source": "test source",
        "url": "https://example.com"
    }

    result = convert_recipe(raw_recipe)

    assert result["name"] == "Test Recipe"
    assert result["ingredients"] == ["flour", "salt", "olive oil"]
    assert result["source_url"] == "https://example.com"