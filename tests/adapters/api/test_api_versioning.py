from fastapi.testclient import TestClient

from bridgeit.adapters.api import main as main_module


def test_openapi_exposes_only_versioned_public_routes() -> None:
    client = TestClient(main_module.app)

    response = client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]

    assert "/api/v1/health" in paths
    assert "/api/v1/requirements" in paths
    assert "/api/v1/requirements/{requirement_id}" in paths
    assert "/api/v1/requirements/{requirement_id}/analyse" in paths
    assert "/api/v1/requirements/{requirement_id}/validate" in paths

    assert "/health" not in paths
    assert "/requirements" not in paths
    assert "/requirements/{requirement_id}" not in paths
    assert "/requirements/{requirement_id}/analyse" not in paths
    assert "/requirements/{requirement_id}/validate" not in paths


def test_legacy_health_route_remains_available() -> None:
    client = TestClient(main_module.app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
