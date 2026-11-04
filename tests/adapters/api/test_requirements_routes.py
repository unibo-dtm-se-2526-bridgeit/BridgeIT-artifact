import pytest
from fastapi.testclient import TestClient

from bridgeit.adapters.api import main as main_module
from bridgeit.infrastructure.persistence.sqlite_requirement_repository import (
    SQLiteRequirementRepository,
)


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Point the app at a fresh, temporary database for each test, instead
    # of the real bridgeit.db -- keeps tests isolated and repeatable.
    test_repository = SQLiteRequirementRepository(tmp_path / "test_bridgeit.db")
    monkeypatch.setattr(main_module, "_repository", test_repository)
    return TestClient(main_module.app)


def test_create_requirement_returns_201_and_submitted_status(client) -> None:
    response = client.post(
        "/api/v1/requirements", json={"text": "The system shall do X"}
    )

    assert response.status_code == 201
    body = response.json()
    assert body["text"] == "The system shall do X"
    assert body["status"] == "Submitted"
    assert "id" in body


def test_get_requirement_returns_the_created_requirement(client) -> None:
    create_response = client.post(
        "/api/v1/requirements", json={"text": "Another requirement"}
    )
    requirement_id = create_response.json()["id"]

    response = client.get(f"/api/v1/requirements/{requirement_id}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == requirement_id
    assert body["text"] == "Another requirement"
    assert body["status"] == "Submitted"


def test_get_requirement_not_found_returns_structured_error(client) -> None:
    response = client.get("/api/v1/requirements/does-not-exist")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "requirement_not_found",
            "message": "No requirement found with the given id.",
        }
    }
