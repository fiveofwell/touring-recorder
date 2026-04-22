import uuid
from schemas.api_schema import Point, PointsPost
from datetime import datetime
import test_utils as util

def test_post_points(device_client):
    tour_id = str(uuid.uuid4())
    point = Point(
            client_point_id=0,
            latitude=34.567,
            longitude=123.456,
            recorded_at=datetime.now()
    )

    pointspost = PointsPost(
        points=[point]
    )

    response = device_client.post(
        f"/api/public/tours/{tour_id}/points",
        json=pointspost.model_dump(mode="json")
    )

    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_post_points_invalid_api_key(client):
    tour_id = str(uuid.uuid4())
    point = Point(
            client_point_id=0,
            latitude=34.567,
            longitude=123.456,
            recorded_at=datetime.now()
    )

    pointspost = PointsPost(
        points=[point]
    )

    response = client.post(
        f"/api/public/tours/{tour_id}/points",
        headers={
            "X-API-KEY": "xxx"
        },
        json=pointspost.model_dump(mode="json")
    )

    assert response.status_code == 401, response.json()
    assert response.json()["detail"] == "Could not validate credentials"


def test_post_points_device_not_found(authenticated_client):
    test_device_name = "test_device"
    response = util.register_device(authenticated_client, test_device_name)
    api_key = response.json()["api_key"]
    device_id = response.json()["device_id"]

    authenticated_client.delete(f"/api/internal/devices/{device_id}")

    authenticated_client.headers["X-API-KEY"] = api_key

    # JWTを削除し、APIキーのみで認証する
    del authenticated_client.headers["Authorization"]

    tour_id = str(uuid.uuid4())
    point = Point(
            client_point_id=0,
            latitude=34.567,
            longitude=123.456,
            recorded_at=datetime.now()
    )

    pointspost = PointsPost(
        points=[point]
    )

    response = authenticated_client.post(
        f"/api/public/tours/{tour_id}/points",
        json=pointspost.model_dump(mode="json")
    )

    assert response.status_code == 401, response.json()
    assert response.json()["detail"] == "Could not validate credentials"
