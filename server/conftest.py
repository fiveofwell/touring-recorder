import sys
import os

# server/ ディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pytest
from db import get_session
from fastapi.testclient import TestClient
from main import app
from sqlmodel import SQLModel, create_engine, Session


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite:///./test_app.db"
    )
    SQLModel.metadata.create_all(engine)

    def override_get_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    yield TestClient(app)
    app.dependency_overrides.clear()

    SQLModel.metadata.drop_all(engine)
    
