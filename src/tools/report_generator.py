class ReportGeneratorTool:

    def generate(
        self,
        user_ingredients: list[str],
        recommendations: list[dict],
        data_source: str,
        fallback_used: bool = False,
        api_error: str | None = None
    ) -> dict:

        if not recommendations:
            return {
                "user_ingredients": user_ingredients,
                "data_source": data_source,
                "fallback_used": fallback_used,
                "api_error": api_error,
                "summary": "No matching recipes were found.",
                "recommendations": []
            }

        best_recipe = recommendations[0]

        return {
            "user_ingredients": user_ingredients,
            "data_source": data_source,
            "fallback_used": fallback_used,
            "api_error": api_error,
            "total_recommendations": len(recommendations),
            "summary": (
                f"The best recommendation is {best_recipe['name']} "
                f"with a match score of {best_recipe['match_score']}%."
            ),
            "recommendations": recommendations
        }