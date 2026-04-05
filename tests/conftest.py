"""Shared pytest fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.routers import items as items_router


@pytest.fixture(autouse=True)
def reset_items_db():
    """Reset the in-memory store before each test to ensure isolation."""
    items_router._db.clear()
    items_router._next_id = 1
    yield


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_app())
