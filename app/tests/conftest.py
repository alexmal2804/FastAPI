from fastapi.testclient import TestClient
from ..main import app
import pytest


@pytest.fixture(scope="function")
def client():
    return TestClient(app)
