# Recipe Recommendation Agent

Recipe Recommendation Agent is a Python-based agent system that recommends recipes based on ingredients provided by the user.

The system receives a list of ingredients, processes the input, compares it with a local recipe database, and returns recipe recommendations with match scores and missing ingredients.

## Features

- Receives ingredients from the user
- Cleans and normalizes ingredient input
- Loads recipes from a local JSON database
- Compares user ingredients with recipe ingredients
- Calculates match scores
- Shows missing ingredients
- Provides recommendations through an API
- Includes Swagger documentation
- Includes basic tests

## Technologies

- Python
- FastAPI
- Swagger UI
- JSON
- Pytest

## Project Structure

```text
src/
  main.py
  agent.py
  schemas.py
  tools/
    ingredient_parser.py
    recipe_database.py
    recipe_matcher.py
    report_generator.py

data/
  recipes.json

tests/
  test_agent.py
  test_ingredient_parser.py


