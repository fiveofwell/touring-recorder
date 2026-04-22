import pytest
from fastapi.testclient import TestClient
import test_utils as util
from main import app

@pytest.fixture
def make_authenticated_client(client):
    def _make(username, password):
        util.create_test_user(client, username, password)
        token = util.get_token(client, username, password).json()["access_token"]
        new_client = TestClient(app)
        new_client.headers["Authorization"] = f"Bearer {token}"
        return new_client
    return _make
