import pytest

from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client() -> TestClient:
    client = TestClient(app)
    yield client
