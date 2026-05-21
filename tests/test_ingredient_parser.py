import pytest

from src.tools.ingredient_parser import IngredientParserTool


def test_parse_ingredients_returns_clean_list():
    parser = IngredientParserTool()

    result = parser.parse("Eggs, Cheese, Tomato")

    assert result == ["eggs", "cheese", "tomato"]


def test_parse_ingredients_removes_duplicates():
    parser = IngredientParserTool()

    result = parser.parse("Eggs, eggs, Cheese")

    assert result == ["eggs", "cheese"]


def test_parse_empty_input_raises_error():
    parser = IngredientParserTool()

    with pytest.raises(ValueError):
        parser.parse("")