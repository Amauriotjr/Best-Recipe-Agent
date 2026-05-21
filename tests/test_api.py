from fastapi.testclient import TestClient

from src import main


class FakeAgent:
    def recommend(self, raw_ingredients: str, max_results: int = 5):
        return {
            "user_ingredients": ["flour", "sugar"],
            "data_source": "fake database",
            "total_recommendations": 1,
            "summary": "The best recommendation is Test Recipe with a match score of 50.0%.",
            "recommendations": [
                {
                    "name": "Test Recipe",
                    "match_score": 50.0,
                    "available_ingredients": ["flour"],
                    "missing_ingredients": ["sugar"]
                }
            ]
        }


client = TestClient(main.app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_recommend_endpoint(monkeypatch):
    monkeypatch.setattr(main, "agent", FakeAgent())

    response = client.post(
        "/recommend",
        json={
            "ingredients": "flour, sugar",
            "max_results": 5
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "summary" in data
    assert "recommendations" in data
    assert data["data_source"] == "fake database"


def test_recommend_endpoint_rejects_empty_input():
    response = client.post(
        "/recommend",
        json={
            "ingredients": "",
            "max_results": 5
        }
    )

    assert response.status_code == 400