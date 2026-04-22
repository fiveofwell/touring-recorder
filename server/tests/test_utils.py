from schemas.api_schema import Point, PointsPost, UserPost, DevicePost
from datetime import datetime

def create_test_tour(client, tour_id):
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
        f"/api/internal/tours/{tour_id}/points",
        json=pointspost.model_dump(mode="json")
    )
    return response


def create_test_user(client, username, password):
    user = UserPost(
        username=username,
        password=password
    )
    response = client.post(
        "/users",
        json=user.model_dump(mode="json")
    )
    return response


def get_token(client, username, password):
    body = {"username": username, "password": password}
    response = client.post(
        "/token",
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        data=body
    )
    return response


def register_device(authenticated_client, device_name):
    device_post = DevicePost(
        device_name=device_name
    )

    response = authenticated_client.post(
        "/api/internal/devices",
        json=device_post.model_dump(mode="json")
    )
    return response


