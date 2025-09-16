import json
import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from src.main import app, models


def test_read_root():
    with TestClient(app) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "CRUDL endpoint"}


fixtures = []

for model in models:
    with open(f"tests/fixtures/{model}.json", "r") as file:
        fixtures.append(json.load(file))


def test_fixtures_loaded():
    assert len(fixtures) == len(models)


def assert_model_item(json: dict, fixture: dict, update=False):
    assert "id" in json
    assert type(json["id"]) is int
    assert "timestamp" in json
    assert type(datetime.fromisoformat(json["timestamp"])) is datetime

    item = fixture["item"]
    if update:
        item.update(fixture["update"])

    for key, value in item.items():
        assert json[key] == value

    return json["id"]


@pytest.mark.parametrize("fixture", fixtures)
def test_create_item(fixture):
    with TestClient(app) as client:
        response = client.post(
            f"/{fixture["path"]}/",
            json=fixture["item"],
        )

    assert response.status_code == 201
    fixture["id"] = assert_model_item(response.json(), fixture)


@pytest.mark.parametrize("fixture", fixtures)
def test_read_items(fixture):
    with TestClient(app) as client:
        response = client.get(f"/{fixture["path"]}/")

    assert response.status_code == 200

    json = response.json()

    assert type(json) is list
    assert len(json) > 0


@pytest.mark.parametrize("fixture", fixtures)
def test_read_item(fixture):
    with TestClient(app) as client:
        response = client.get(f"/{fixture["path"]}/{fixture["id"]}")

    assert response.status_code == 200
    id = assert_model_item(response.json(), fixture)
    assert id == fixture["id"]


@pytest.mark.parametrize("fixture", fixtures)
def test_update_item(fixture):
    with TestClient(app) as client:
        response = client.put(
            f"/{fixture["path"]}/{fixture["id"]}",
            json=fixture["update"],
        )

    assert response.status_code == 200
    id = assert_model_item(response.json(), fixture, update=fixture["update"])
    assert id == fixture["id"]


@pytest.mark.parametrize("fixture", fixtures)
def test_delete_item(fixture):
    with TestClient(app) as client:
        response = client.delete(f"/{fixture["path"]}/{fixture["id"]}")

    assert response.status_code == 204


@pytest.mark.parametrize("fixture", fixtures)
def test_create_item_with_invalid_body(fixture):
    with TestClient(app) as client:
        response = client.post(
            f"/{fixture["path"]}/",
            json=fixture["update"] | {"test": "invalid"},
        )

    assert response.status_code == 422
