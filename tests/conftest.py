import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app
from app.seed_db import setup_db

@pytest.fixture(scope="module")
def test_app():
    setup_db()
    client = TestClient(app)
    yield client

