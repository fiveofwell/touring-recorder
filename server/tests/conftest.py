import sys
import os

# server/ ディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import StaticPool

import tests.test_utils as util
from db import get_session
from redis_client import get_redis_client
from main import app

class MockRedisClient:
    def __init__(self) -> None:
        self.store = {}  # シンプルな辞書を使用してキーと値を保存
        pass

    def incr(self, key):
        value = self.store.get(key, 0) + 1
        self.store[key] = value
        return value

    def expire(self, key, window):
        pass  # 何もしない

    def get(self, key):
        return self.store.get(key)
    
    def setex(self, key, time, value):
        self.store[key] = value  # キーと値のみ保存

@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)

    def override_get_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session


    mock_redis_client = MockRedisClient()
    def override_get_redis_client():
        # テスト用のモックRedisクライアントを返す(テストごとに状態をリセット)
        return mock_redis_client

    app.dependency_overrides[get_redis_client] = override_get_redis_client
    yield TestClient(app)
    app.dependency_overrides.clear()

    SQLModel.metadata.drop_all(engine)
    

@pytest.fixture
def authenticated_client(client):
    test_username = "test_user"
    test_password = "secret"
    util.create_test_user(client, test_username, test_password)
    token = util.get_token(client, test_username, test_password).json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client


@pytest.fixture
def device_client(client, authenticated_client):
    test_device_name = "test_device"
    api_key = util.register_device(authenticated_client, test_device_name).json()["api_key"]
    client.headers["X-API-KEY"] = api_key
    return client
