from fastapi.testclient import TestClient

from app.main import app


def test_health() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_categories_list() -> None:
    client = TestClient(app)
    response = client.get("/support/categories")
    assert response.status_code == 200
    assert "account_access" in response.json()


def test_analyze_matches_readme_example() -> None:
    client = TestClient(app)
    response = client.post(
        "/support/analyze",
        json={
            "message": "I can't access my account after password reset.",
            "customer_id": "12345",
            "channel": "web",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["category"] == "account_access"
    assert body["priority"] == "high"
    assert body["needs_human_review"] is True
    assert body["suggested_reply"]
