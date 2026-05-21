# AI Recipe Recommendation Agent

AI Recipe Recommendation Agent is a Python-based agent system that recommends recipes based on ingredients provided by the user.

The system receives a list of ingredients, processes the input, retrieves recipe data from MongoDB, compares ingredients, calculates match scores, and returns structured recipe recommendations through a FastAPI API.

This project was developed as an AI- and agent-based Python software system. It demonstrates tool usage, database access, external data conversion, API development, testing, and deployment preparation.

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
- the database source used;
- links to original recipe sources when available.

## Main Features

- Receives ingredients from the user
- Cleans and normalizes ingredient input
- Uses an agent-based workflow
- Uses MongoDB as the main recipe database
- Imports recipe data from an external GitHub dataset
- Converts external JSON recipe data into the internal project format
- Removes quantities, fractions, and measurement units from ingredient names
- Stores normalized ingredients in MongoDB for search
- Compares user ingredients with recipe ingredients
- Calculates recipe match scores
- Avoids false ingredient matches such as `flour` matching `rice flour`
- Avoids false ingredient matches such as `peanut butter` matching `butter`
- Shows available and missing ingredients
- Provides API routes using FastAPI
- Provides Swagger UI for testing
- Includes automated tests with pytest

## Technologies Used

- Python
- FastAPI
- Swagger UI
- Uvicorn
- MongoDB
- PyMongo
- Python Dotenv
- JSON
- Pytest
- Git
- GitHub

## Agent-Based Approach

The system uses an agent-based workflow.

The main agent is responsible for coordinating the tools and controlling the recommendation process. The user does not interact directly with each internal tool. Instead, the user sends ingredients to the API, and the agent decides how to process the request.

The workflow is:

```text
User input
→ Recipe Recommendation Agent
→ Ingredient Parser Tool
→ MongoDB Recipe Database Tool
→ Recipe Matcher Tool
→ Report Generator Tool
→ Final recommendation response
```

The agent performs the following responsibilities:

1. Receives raw ingredient input from the user.
2. Calls the Ingredient Parser Tool to clean the input.
3. Calls the MongoDB Recipe Database Tool to retrieve candidate recipes.
4. Calls the Recipe Matcher Tool to calculate recipe compatibility.
5. Calls the Report Generator Tool to create the final structured response.

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

### Ingredient Normalizer Tool

The Ingredient Normalizer Tool normalizes ingredient names so they can be compared consistently.

For example:

```text
eggs → egg
tomatoes → tomato
all-purpose flour → all purpose flour
```

This improves matching while avoiding incorrect partial matches.

For example:

```text
flour does not match brown rice flour
flour does not match flour tortilla
peanut butter does not match butter
```

### MongoDB Recipe Database Tool

The MongoDB Recipe Database Tool connects to MongoDB and retrieves recipe candidates.

MongoDB is used as the main database because the full converted recipe dataset is too large to store directly in GitHub.

The tool searches recipes using normalized ingredients stored in the database.

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

The matcher uses strict ingredient comparison to avoid false positives.

### Report Generator Tool

The Report Generator Tool creates the final structured response.

The response includes:

- user ingredients;
- data source;
- total recommendations;
- summary;
- recommended recipes;
- available ingredients;
- missing ingredients;
- source links when available.

## External Data Source

This project uses recipe data adapted from the public GitHub repository:

```text
https://github.com/dpapathanasiou/recipes
```

The dataset is used as the main recipe source.

The external repository itself is not committed directly into this project repository. It is downloaded locally into:

```text
data/external/recipes-github/
```

This folder is ignored by Git using `.gitignore`.

The external dataset is first converted into the internal project format and then imported into MongoDB.

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
- converts the data into the internal project format;
- saves the result locally in `data/recipes.json`;
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

## MongoDB Import Process

After the external dataset is converted into `data/recipes.json`, the recipes are imported into MongoDB using:

```text
scripts/import_recipes_to_mongodb.py
```

During the MongoDB import process, the system:

- reads the converted `data/recipes.json` file;
- adds a `normalized_ingredients` field to each recipe;
- inserts recipes into MongoDB in batches;
- creates indexes for better search performance.

The full generated `data/recipes.json` file is not committed to GitHub because it is larger than GitHub's file size limit.

Instead, the project includes scripts that allow the database to be recreated locally.

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
│       ├── ingredient_normalizer.py
│       ├── recipe_mongodb.py
│       ├── recipe_matcher.py
│       └── report_generator.py
│
├── scripts/
│   ├── import_github_recipes.py
│   └── import_recipes_to_mongodb.py
│
├── data/
│   ├── recipes_sample.json
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
├── .env.example
├── README.md
├── requirements.txt
└── .gitignore
```

## Important GitHub Note

The full file below is generated locally and should not be committed to GitHub:

```text
data/recipes.json
```

This file can be larger than 100 MB, which exceeds GitHub's file size limit.

The following files and folders are ignored by Git:

```text
data/recipes.json
data/external/recipes-github/
.env
venv/
__pycache__/
.pytest_cache/
```

The project stores the large recipe dataset in MongoDB instead of GitHub.

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DATABASE=recipe_agent
MONGODB_COLLECTION=recipes
```

The `.env` file must not be committed to GitHub because it contains sensitive connection information.

A safe example file should be included as:

```text
.env.example
```

Example `.env.example`:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/
MONGODB_DATABASE=recipe_agent
MONGODB_COLLECTION=recipes
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
python -m pip install -r requirements.txt
```

## Preparing the External Dataset

Create the external data folder:

```bash
mkdir -p data/external
```

On Windows PowerShell:

```powershell
mkdir data\external
```

Clone the external recipe dataset:

```bash
git clone --depth 1 https://github.com/dpapathanasiou/recipes.git data/external/recipes-github
```

Run the conversion script:

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

## Importing Recipes into MongoDB

After creating `data/recipes.json`, import the converted recipes into MongoDB:

```bash
python scripts/import_recipes_to_mongodb.py --clear
```

The `--clear` option removes existing recipes from the collection before importing the new data.

If the import works correctly, the terminal will show a message similar to:

```text
Imported 50000 recipes into MongoDB.
Database: recipe_agent
Collection: recipes
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

### GET `/database/status`

Checks the MongoDB connection and returns database information.

Example response:

```json
{
  "status": "connected",
  "database": "recipe_agent",
  "collection": "recipes",
  "total_recipes": 50000
}
```

### GET `/recipes/search`

Searches candidate recipes from MongoDB using one or more ingredients.

Example:

```text
http://127.0.0.1:8000/recipes/search?ingredients=flour,sugar,eggs&limit=10
```

### POST `/recommend`

Recommends recipes based on the ingredients provided by the user.

Example request:

```json
{
  "ingredients": "flour, sugar, eggs, butter",
  "max_results": 5
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
  "data_source": "MongoDB recipe database",
  "total_recommendations": 5,
  "summary": "The best recommendation is Example Recipe with a match score of 75.0%.",
  "recommendations": [
    {
      "id": null,
      "name": "Example Recipe",
      "category": "external",
      "area": "unknown",
      "difficulty": "unknown",
      "source": "allrecipes.com",
      "match_score": 75.0,
      "available_ingredients": [
        "flour",
        "sugar",
        "eggs"
      ],
      "missing_ingredients": [
        "butter"
      ],
      "original_ingredients": [
        "1 cup flour",
        "1 cup sugar",
        "2 eggs",
        "1/2 cup butter"
      ],
      "source_url": "https://example.com"
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

Recommended test:

```json
{
  "ingredients": "flour, sugar, eggs, butter",
  "max_results": 5
}
```

You can also test:

```json
{
  "ingredients": "peanut butter, bread",
  "max_results": 5
}
```

And:

```json
{
  "ingredients": "tomato, cheese, pasta",
  "max_results": 5
}
```

## Running Automated Tests

Run all tests:

```bash
python -m pytest
```

Using `python -m pytest` is recommended because it works more reliably on Windows virtual environments.

The tests verify:

- ingredient parsing;
- duplicate ingredient removal;
- invalid input handling;
- ingredient cleaning during import;
- recipe matching;
- strict ingredient matching;
- plural and singular ingredient matching;
- agent workflow with a fake database;
- API endpoints;
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

The agent then sends this list to the MongoDB Recipe Database Tool. MongoDB returns candidate recipes as dictionaries.

Each recipe contains fields such as:

```json
{
  "name": "Recipe Name",
  "ingredients": ["flour", "sugar", "eggs"],
  "normalized_ingredients": ["flour", "sugar", "egg"],
  "category": "external",
  "difficulty": "unknown"
}
```

The Recipe Matcher Tool compares the user's normalized ingredients with each recipe's normalized ingredients and returns structured recommendation data.

The final response is returned as JSON through the FastAPI API.

## Error Handling

The system handles several error cases:

- empty ingredient input;
- missing MongoDB connection string;
- unavailable MongoDB database;
- invalid database configuration;
- recipes without valid ingredients;
- no matching recipes found.

If MongoDB is not configured correctly, the system returns an error explaining that `MONGODB_URI` is missing or invalid.

## Deployment Preparation

The current version is prepared as a local API application.

It can be executed locally using:

```bash
uvicorn src.main:app --reload
```

This deployment approach is suitable for controlled testing because the user can run the API locally, test it through Swagger, and verify the output before using it in a real environment.

The MongoDB connection is configured through environment variables, which makes the application easier to deploy safely.

## Proposed Deployment Strategy

The recommended deployment strategy is a staged release.

First, the system should be tested locally using Swagger and a MongoDB test database. After local testing, the full recipe dataset should be imported into MongoDB. Then, the system can be deployed to a controlled environment such as:

- local server;
- Docker container;
- cloud web service;
- API-based assistant.

This strategy reduces risk because the application logic can be tested separately from the full production database.

## Version Control

Git is used to track the development process.

Recommended commit history:

```bash
git add .
git commit -m "Create initial FastAPI recipe recommendation agent"

git add .
git commit -m "Add external recipe dataset import script"

git add .
git commit -m "Improve ingredient cleaning and recipe matching"

git add .
git commit -m "Replace external API with MongoDB recipe database"

git add .
git commit -m "Add MongoDB import workflow"

git add .
git commit -m "Update README documentation"
```

Before pushing to GitHub, confirm that the large dataset is not staged:

```bash
git status
```

Do not push:

```text
data/recipes.json
data/external/recipes-github/
.env
```

## Project Status

Current version: `0.4.0`

The system currently supports:

- recipe recommendation through MongoDB;
- external dataset import;
- data conversion;
- ingredient cleaning;
- normalized database search;
- strict ingredient matching;
- FastAPI routes;
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

The external dataset is used as the recipe data source. The data is converted into the internal format required by this project and then imported into MongoDB.

The external repository is not included directly in this repository. It should be cloned separately into:

```text
data/external/recipes-github/
```

## License

This project is for academic and educational purposes.