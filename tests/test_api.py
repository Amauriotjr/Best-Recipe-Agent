from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_recommend_endpoint_with_local_database():
    response = client.post(
        "/recommend",
        json={
            "ingredients": "flour, sugar, eggs, butter",
            "max_results": 5,
            "use_online_api": False
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "summary" in data
    assert "recommendations" in data
    assert data["data_source"] == "local database"


def test_recommend_endpoint_rejects_empty_input():
    response = client.post(
        "/recommend",
        json={
            "ingredients": "",
            "max_results": 3,
            "use_online_api": False
        }
    )

    assert response.status_code == 400


def test_local_recipes_endpoint():
    response = client.get("/recipes/local?limit=5")

    assert response.status_code == 200

    data = response.json()

    assert "recipes" in data
    assert "total_recipes" in data