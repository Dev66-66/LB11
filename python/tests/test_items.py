import gc
import os
import tempfile
import pytest
import routes.item_routes as item_routes_module
from repositories.item_repository import ItemRepository
from services.item_service import ItemService
from app import app as flask_app

API = "/items/api/items"


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)

    test_repo = ItemRepository(db_path)
    test_service = ItemService(test_repo)
    item_routes_module.repository = test_repo
    item_routes_module.service = test_service

    flask_app.config["TESTING"] = True
    yield flask_app

    # Force-close SQLite connections (needed on Windows)
    gc.collect()
    try:
        os.unlink(db_path)
    except PermissionError:
        pass


@pytest.fixture
def client(app):
    return app.test_client()


def _create(client, title="Test Item", description="Test Desc"):
    return client.post(API, json={"title": title, "description": description})


# --- Health ---

def test_health_endpoint_status(client):
    res = client.get("/health")
    assert res.status_code == 200


def test_health_endpoint_body(client):
    res = client.get("/health")
    assert res.get_json() == {"status": "ok"}


# --- GET all items ---

def test_get_all_items_empty_list(client):
    res = client.get(API)
    assert res.status_code == 200
    assert res.get_json() == []


def test_get_all_items_returns_list_type(client):
    res = client.get(API)
    assert isinstance(res.get_json(), list)


def test_get_all_items_after_create(client):
    _create(client, "Alpha")
    _create(client, "Beta")
    res = client.get(API)
    data = res.get_json()
    assert len(data) == 2


# --- POST create ---

def test_create_item_status_201(client):
    res = _create(client)
    assert res.status_code == 201


def test_create_item_returns_id(client):
    res = _create(client)
    data = res.get_json()
    assert "id" in data
    assert isinstance(data["id"], int)


def test_create_item_returns_title(client):
    res = _create(client, title="My Title")
    data = res.get_json()
    assert data["title"] == "My Title"


def test_create_item_returns_description(client):
    res = _create(client, description="My Desc")
    data = res.get_json()
    assert data["description"] == "My Desc"


def test_create_item_empty_title_returns_400(client):
    res = client.post(API, json={"title": "", "description": "desc"})
    assert res.status_code == 400


def test_create_item_whitespace_title_returns_400(client):
    res = client.post(API, json={"title": "   ", "description": "desc"})
    assert res.status_code == 400


def test_create_item_no_body_returns_400(client):
    res = client.post(API, content_type="application/json", data="")
    assert res.status_code == 400


def test_create_item_no_json_content_type_returns_4xx(client):
    res = client.post(API, data="title=Test")
    assert res.status_code in (400, 415)


def test_create_duplicate_items_both_succeed(client):
    res1 = _create(client, title="Dup")
    res2 = _create(client, title="Dup")
    assert res1.status_code == 201
    assert res2.status_code == 201
    assert res1.get_json()["id"] != res2.get_json()["id"]


# --- GET by ID ---

def test_get_item_by_id_status_200(client):
    item_id = _create(client).get_json()["id"]
    res = client.get(f"{API}/{item_id}")
    assert res.status_code == 200


def test_get_item_by_id_correct_fields(client):
    _create(client, title="Field Test", description="Desc Test")
    item_id = client.get(API).get_json()[0]["id"]
    res = client.get(f"{API}/{item_id}")
    data = res.get_json()
    assert "id" in data
    assert "title" in data
    assert "description" in data


def test_get_item_by_id_correct_values(client):
    item_id = _create(client, title="Exact", description="Exact Desc").get_json()["id"]
    data = client.get(f"{API}/{item_id}").get_json()
    assert data["title"] == "Exact"
    assert data["description"] == "Exact Desc"


def test_get_item_not_found_returns_404(client):
    res = client.get(f"{API}/99999")
    assert res.status_code == 404


def test_get_item_not_found_has_error_field(client):
    res = client.get(f"{API}/99999")
    assert "error" in res.get_json()


# --- PUT update ---

def test_update_item_status_200(client):
    item_id = _create(client).get_json()["id"]
    res = client.put(f"{API}/{item_id}", json={"title": "Updated", "description": ""})
    assert res.status_code == 200


def test_update_item_changes_data(client):
    item_id = _create(client, title="Old", description="Old Desc").get_json()["id"]
    client.put(f"{API}/{item_id}", json={"title": "New", "description": "New Desc"})
    data = client.get(f"{API}/{item_id}").get_json()
    assert data["title"] == "New"
    assert data["description"] == "New Desc"


def test_update_item_not_found_returns_404(client):
    res = client.put(f"{API}/99999", json={"title": "X", "description": ""})
    assert res.status_code == 404


def test_update_item_empty_title_returns_400(client):
    item_id = _create(client).get_json()["id"]
    res = client.put(f"{API}/{item_id}", json={"title": "", "description": ""})
    assert res.status_code == 400


# --- DELETE ---

def test_delete_item_status_204(client):
    item_id = _create(client).get_json()["id"]
    res = client.delete(f"{API}/{item_id}")
    assert res.status_code == 204


def test_delete_item_not_found_returns_404(client):
    res = client.delete(f"{API}/99999")
    assert res.status_code == 404


def test_delete_then_get_returns_404(client):
    item_id = _create(client).get_json()["id"]
    client.delete(f"{API}/{item_id}")
    res = client.get(f"{API}/{item_id}")
    assert res.status_code == 404


def test_delete_reduces_list_count(client):
    id1 = _create(client, "A").get_json()["id"]
    _create(client, "B")
    client.delete(f"{API}/{id1}")
    items = client.get(API).get_json()
    assert len(items) == 1
