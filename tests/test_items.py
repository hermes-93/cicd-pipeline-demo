"""Tests for the items CRUD endpoints."""

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _create_item(client, name="Widget", price=9.99, description="A test widget"):
    return client.post("/items/", json={"name": name, "price": price, "description": description})


# ---------------------------------------------------------------------------
# List
# ---------------------------------------------------------------------------


def test_list_items_empty(client):
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == []


def test_list_items_returns_created(client):
    _create_item(client)
    _create_item(client, name="Gadget", price=19.99)
    items = client.get("/items/").json()
    assert len(items) == 2


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------


def test_create_item_returns_201(client):
    response = _create_item(client)
    assert response.status_code == 201


def test_create_item_response_shape(client):
    data = _create_item(client).json()
    assert data["id"] == 1
    assert data["name"] == "Widget"
    assert data["price"] == 9.99
    assert data["description"] == "A test widget"


def test_create_item_auto_increments_id(client):
    first = _create_item(client).json()
    second = _create_item(client, name="Gadget", price=1.0).json()
    assert second["id"] == first["id"] + 1


@pytest.mark.parametrize(
    "bad_payload",
    [
        {"name": "", "price": 5.0},  # empty name
        {"name": "x", "price": -1.0},  # negative price
        {"name": "x", "price": 0},  # zero price
        {"price": 5.0},  # missing name
        {"name": "x"},  # missing price
    ],
)
def test_create_item_validates_input(client, bad_payload):
    response = client.post("/items/", json=bad_payload)
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Get
# ---------------------------------------------------------------------------


def test_get_item_returns_200(client):
    item_id = _create_item(client).json()["id"]
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200


def test_get_item_not_found(client):
    response = client.get("/items/999")
    assert response.status_code == 404


def test_get_item_returns_correct_data(client):
    created = _create_item(client, name="SpecialItem", price=42.0).json()
    fetched = client.get(f"/items/{created['id']}").json()
    assert fetched == created


# ---------------------------------------------------------------------------
# Update
# ---------------------------------------------------------------------------


def test_update_item_name(client):
    item_id = _create_item(client).json()["id"]
    response = client.patch(f"/items/{item_id}", json={"name": "Updated"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"


def test_update_item_price(client):
    item_id = _create_item(client).json()["id"]
    response = client.patch(f"/items/{item_id}", json={"price": 99.99})
    assert response.json()["price"] == 99.99


def test_update_item_preserves_other_fields(client):
    item = _create_item(client, name="Keep", price=5.0, description="keep me").json()
    updated = client.patch(f"/items/{item['id']}", json={"price": 10.0}).json()
    assert updated["name"] == "Keep"
    assert updated["description"] == "keep me"


def test_update_item_not_found(client):
    response = client.patch("/items/999", json={"name": "Ghost"})
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------


def test_delete_item_returns_204(client):
    item_id = _create_item(client).json()["id"]
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204


def test_delete_item_removes_it(client):
    item_id = _create_item(client).json()["id"]
    client.delete(f"/items/{item_id}")
    assert client.get(f"/items/{item_id}").status_code == 404


def test_delete_item_not_found(client):
    response = client.delete("/items/999")
    assert response.status_code == 404
