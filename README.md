# AI Recipe Recommendation Agent

AI Recipe Recommendation Agent is a Python-based agent system that recommends recipes based on ingredients provided by the user.

The system receives a list of ingredients, processes the input, retrieves recipe data from an online API or a local database, compares ingredients, calculates match scores, and returns structured recipe recommendations.

This project was developed as an AI- and agent-based Python software system. It demonstrates tool usage, external data retrieval, local data processing, API development, testing, and deployment preparation.

## Project Goal

The goal of this project is to help users discover recipes they can prepare using ingredients they already have.

The user provides ingredients such as:

```text
flour, sugar, eggs, butter
```

The system then recommends recipes and shows:

- the best matching recipes;
- the match score for each recipe;
- available ingredients;
- missing ingredients;
- the data source used;
- links to online recipes when available.

## Main Features

- Receives ingredients from the user
- Cleans and normalizes ingredient input
- Uses an agent-based workflow
- Uses TheMealDB API as an online recipe source
- Uses a local JSON recipe database as fallback
- Imports recipe data from an external GitHub dataset
- Converts external JSON recipe data into the internal project format
- Removes quantities, fractions, and measurement units from ingredients
- Compares user ingredients with recipe ingredients
- Calculates recipe match scores
- Shows available and missing ingredients
- Provides API routes using FastAPI
- Provides Swagger UI for testing
- Includes automated tests with pytest

## Technologies Used

- Python
- FastAPI
- Swagger UI
- Uvicorn
- Requests
- JSON
- Pytest
- Git
- GitHub

## Agent-Based Approach

The system uses an agent-based workflow.

The main agent is responsible for coordinating the tools and controlling the recommendation process. The user does not interact directly with each tool. Instead, the user sends ingredients to the API, and the agent decides how to process the request.

The workflow is:

```text
User input
→ Recipe Recommendation Agent
→ Ingredient Parser Tool
→ TheMealDB API Tool or Local Recipe Database Tool
→ Recipe Matcher Tool
→ Report Generator Tool
→ Final recommendation response
```

The agent performs the following responsibilities:

1. Receives raw ingredient input from the user.
2. Calls the Ingredient Parser Tool to clean and normalize the input.
3. Tries to retrieve recipes from TheMealDB API when online mode is enabled.
4. Uses the local recipe database if the online API is disabled or unavailable.
5. Calls the Recipe Matcher Tool to calculate recipe compatibility.
6. Calls the Report Generator Tool to create the final structured response.

## Tools Used by the System

### Ingredient Parser Tool

The Ingredient Parser Tool converts raw user input into a clean list of ingredients.

Example input:

```text
Eggs, Flour, Sugar
```

Example output:

```python
["eggs", "flour", "sugar"]
```

This tool removes extra spaces, converts text to lowercase, and removes duplicate ingredients.

### Recipe API Tool

The Recipe API Tool connects to TheMealDB API and retrieves online recipes based on a main ingredient.

The API response is received in JSON format and converted into the internal recipe format used by the system.

### Local Recipe Database Tool

The Local Recipe Database Tool reads recipes from:

```text
data/recipes.json
```

This local database is used when:

- the user disables the online API;
- the external API is unavailable;
- the system needs fallback data.

### Recipe Matcher Tool

The Recipe Matcher Tool compares the user's ingredients with the ingredients required by each recipe.

The match score is calculated using the following idea:

```text
match score = available ingredients / required ingredients
```

For example:

```text
User ingredients:
flour, sugar, eggs

Recipe ingredients:
flour, sugar, eggs, butter

Match score:
3 / 4 = 75%
```

The matcher also supports partial ingredient matching. For example, if a recipe has `all-purpose flour` and the user enters `flour`, the system can still identify a match.

### Report Generator Tool

The Report Generator Tool creates the final structured response.

The response includes:

- user ingredients;
- data source;
- fallback status;
- API error, if any;
- total recommendations;
- summary;
- recommended recipes;
- available ingredients;
- missing ingredients;
- source links when available.

## External Data Sources

This project uses two external data sources.

### TheMealDB API

TheMealDB API is used as an online recipe source.

The system searches recipes using the first ingredient provided by the user. After retrieving recipes, the agent applies its own matching and ranking logic using all ingredients entered by the user.

### GitHub Recipe Dataset

This project also uses recipe data adapted from the public GitHub repository:

```text
https://github.com/dpapathanasiou/recipes
```

The dataset is used as a large local recipe source.

The external repository itself is not committed directly into this project repository. It is downloaded locally into:

```text
data/external/recipes-github/
```

This folder is ignored by Git using `.gitignore`.

The converted recipe database is stored in:

```text
data/recipes.json
```

## Data Conversion Process

The external GitHub dataset uses a different JSON structure from this project.

The import script is responsible for converting the external dataset into the internal format used by the agent.

The script is located at:

```text
scripts/import_github_recipes.py
```

During conversion, the system:

- reads all recipe JSON files from the external dataset;
- extracts recipe names;
- extracts ingredient lists;
- extracts instructions;
- extracts source URLs;
- removes duplicate recipes;
- removes invalid recipes;
- converts the data into the internal format;
- saves the result in `data/recipes.json`;
- creates an import summary in `data/recipes_import_summary.json`.

The ingredient cleaning process removes:

- quantities;
- fractions;
- Unicode fractions;
- measurement units;
- preparation details;
- unnecessary punctuation.

Example conversions:

```text
"1/2 cup flour" → "flour"
"½ teaspoon salt" → "salt"
"3 tablespoons olive oil" → "olive oil"
"3/4 cup very warm water" → "water"
"2 teaspoons sugar" → "sugar"
```

This conversion improves consistency and helps the matcher compare user ingredients with recipe ingredients more accurately.

## Project Structure

```text
ai-recipe-recommendation-agent/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── agent.py
│   ├── schemas.py
│   │
│   └── tools/
│       ├── __init__.py
│       ├── ingredient_parser.py
│       ├── recipe_api.py
│       ├── recipe_database.py
│       ├── recipe_matcher.py
│       └── report_generator.py
│
├── scripts/
│   └── import_github_recipes.py
│
├── data/
│   ├── recipes.json
│   ├── recipes_import_summary.json
│   └── external/
│       └── recipes-github/
│
├── tests/
│   ├── test_agent.py
│   ├── test_api.py
│   ├── test_import_github_recipes.py
│   ├── test_ingredient_parser.py
│   └── test_recipe_matcher.py
│
├── README.md
├── requirements.txt
└── .gitignore
```

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/ai-recipe-recommendation-agent.git
cd ai-recipe-recommendation-agent
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Importing the External Recipe Dataset

Create the external data folder:

```bash
mkdir -p data/external
```

Clone the external recipe dataset:

```bash
git clone --depth 1 https://github.com/dpapathanasiou/recipes.git data/external/recipes-github
```

On Windows PowerShell:

```powershell
mkdir data\external
git clone --depth 1 https://github.com/dpapathanasiou/recipes.git data\external\recipes-github
```

Run the import script:

```bash
python scripts/import_github_recipes.py
```

This command generates or updates:

```text
data/recipes.json
data/recipes_import_summary.json
```

To test the import process with a smaller number of recipes:

```bash
python scripts/import_github_recipes.py --limit 100
```

For the final version, import all available recipes:

```bash
python scripts/import_github_recipes.py
```

## Running the Application

Start the API server:

```bash
uvicorn src.main:app --reload
```

Open Swagger UI in the browser:

```text
http://127.0.0.1:8000/docs
```

The Swagger page allows the user to test all API routes directly in the browser.

## API Endpoints

### GET `/`

Returns a welcome message and basic API information.

Example:

```text
http://127.0.0.1:8000/
```

### GET `/health`

Checks if the API is running.

Example response:

```json
{
  "status": "ok"
}
```

### GET `/recipes/local`

Returns recipes from the local database.

Example:

```text
http://127.0.0.1:8000/recipes/local?limit=5
```

### GET `/external/search/{ingredient}`

Searches recipes from TheMealDB API using one main ingredient.

Example:

```text
http://127.0.0.1:8000/external/search/chicken
```

### POST `/recommend`

Recommends recipes based on the ingredients provided by the user.

Example request using the local database:

```json
{
  "ingredients": "flour, sugar, eggs, butter",
  "max_results": 5,
  "use_online_api": false
}
```

Example request using the online API:

```json
{
  "ingredients": "chicken, rice, tomato",
  "max_results": 5,
  "use_online_api": true
}
```

Example response:

```json
{
  "user_ingredients": [
    "flour",
    "sugar",
    "eggs",
    "butter"
  ],
  "data_source": "local database",
  "fallback_used": false,
  "api_error": null,
  "total_recommendations": 5,
  "summary": "The best recommendation is Example Recipe with a match score of 75.0%.",
  "recommendations": [
    {
      "id": null,
      "name": "Example Recipe",
      "category": "external",
      "area": "unknown",
      "difficulty": "unknown",
      "source": "local database",
      "match_score": 75.0,
      "available_ingredients": [
        "flour",
        "sugar",
        "eggs"
      ],
      "missing_ingredients": [
        "butter"
      ],
      "original_ingredients": null,
      "image_url": null,
      "source_url": "https://example.com",
      "youtube_url": null
    }
  ]
}
```

## Testing with Swagger

After running the application, open:

```text
http://127.0.0.1:8000/docs
```

Then test the `POST /recommend` endpoint.

Recommended test using local database:

```json
{
  "ingredients": "flour, sugar, eggs, butter",
  "max_results": 5,
  "use_online_api": false
}
```

Recommended test using online API:

```json
{
  "ingredients": "chicken, rice, tomato",
  "max_results": 5,
  "use_online_api": true
}
```

## Running Automated Tests

Run all tests:

```bash
pytest
```

The tests verify:

- ingredient parsing;
- duplicate ingredient removal;
- invalid input handling;
- ingredient cleaning during import;
- recipe matching;
- partial ingredient matching;
- local database recommendation;
- API endpoints;
- local recipe endpoint;
- dataset conversion logic.

## Input and Output Handling

The system receives user input as a string.

Example:

```text
flour, sugar, eggs, butter
```

The Ingredient Parser Tool converts this string into a list:

```python
["flour", "sugar", "eggs", "butter"]
```

The agent then sends this list to the API tool or local database tool. Recipes are loaded as dictionaries, and each recipe contains fields such as:

```json
{
  "name": "Recipe Name",
  "ingredients": ["flour", "sugar", "eggs"],
  "category": "external",
  "difficulty": "unknown"
}
```

The matcher compares the user's ingredients with each recipe and returns structured recommendation data.

The final response is returned as JSON through the FastAPI API.

## Error Handling

The system handles several error cases:

- empty ingredient input;
- missing local recipe database;
- invalid recipe database format;
- unavailable external API;
- failed external API request;
- recipes without valid ingredients.

When the online API fails, the system uses the local recipe database as fallback.

## Deployment Preparation

The current version is prepared as a local API application.

It can be executed locally using:

```bash
uvicorn src.main:app --reload
```

This deployment approach is suitable for controlled testing because the user can run the API locally, test it through Swagger, and verify the output before using it in a real environment.

In the future, the system could be deployed as:

- a Docker container;
- a cloud web service;
- an API-based assistant;
- a public recipe recommendation service.

## Proposed Deployment Strategy

The recommended deployment strategy is a staged release.

First, the system should be tested locally using the local recipe database and Swagger. After local testing, the online API integration should be tested. Then, the system can be deployed to a controlled environment such as a local server, Docker container, or a cloud platform.

This strategy reduces risk because the system can still work with the local database if the external API becomes unavailable.

## Version Control

Git is used to track the development process.

Recommended commit history:

```bash
git add .
git commit -m "Create initial FastAPI recipe recommendation agent"

git add .
git commit -m "Add TheMealDB API integration with local fallback"

git add .
git commit -m "Add external recipe dataset import script"

git add .
git commit -m "Improve ingredient cleaning and recipe matching"

git add .
git commit -m "Add tests for API and dataset import workflow"

git add .
git commit -m "Update README documentation"
```

## Project Status

Current version: `0.3.0`

The system currently supports:

- local recipe recommendation;
- online recipe search through TheMealDB API;
- local fallback database;
- external dataset import;
- data conversion;
- ingredient cleaning;
- Swagger testing;
- automated tests.

## Future Improvements

Possible future improvements include:

- filtering recipes by category;
- filtering recipes by difficulty;
- filtering recipes by cuisine;
- nutrition information;
- better natural language ingredient matching;
- user accounts;
- saved favorite recipes;
- frontend interface;
- Docker deployment.

## External Dataset Credit

This project uses recipe data adapted from the public GitHub repository:

```text
https://github.com/dpapathanasiou/recipes
```

The external dataset is used only as a local recipe data source. The data is converted into the internal format required by this project.

The external repository is not included directly in this repository. It should be cloned separately into:

```text
data/external/recipes-github/
```