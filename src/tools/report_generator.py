class ReportGeneratorTool:

    def generate(
        self,
        user_ingredients: list[str],
        recommendations: list[dict],
        data_source: str
    ) -> dict:

        if not recommendations:
            return {
                "user_ingredients": user_ingredients,
                "data_source": data_source,
                "total_recommendations": 0,
                "summary": "No matching recipes were found.",
                "recommendations": []
            }

        best_recipe = recommendations[0]

        return {
            "user_ingredients": user_ingredients,
            "data_source": data_source,
            "total_recommendations": len(recommendations),
            "summary": (
                f"The best recommendation is {best_recipe['name']} "
                f"with a match score of {best_recipe['match_score']}%."
            ),
            "recommendations": recommendations
        }