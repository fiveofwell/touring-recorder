from schemas.api_schema import Point, PointsPost
from datetime import datetime

def create_test_tour(client, tour_id):
    point = Point(
            client_point_id=0,
            latitude=34.567,
            longitude=123.456,
            timestamp=datetime.now()
    )

    pointspost = PointsPost(
        device_id="test_device",
        points=[point]
    )

    response = client.post(
        f"/api/internal/tours/{tour_id}",
        json=pointspost.model_dump(mode="json")
    )
    return response


def create_invalid_test_tour(client, tour_id):
    invalid_data = {
        "device_id": "test_device",
        "points": [
            {
                "client_point_id": -1,
                "latitude": "abcdef",
                "longitude": "abcdef",
                "timestamp": "datetime"
            }
        ]
    }

    response = client.post(
        f"/api/internal/tours/{tour_id}",
        json=invalid_data
    )
    return response


def create_test_tour_with_apikey(client, tour_id, apikey):
    point = Point(
            client_point_id=0,
            latitude=34.567,
            longitude=123.456,
            timestamp=datetime.now()
    )

    pointspost = PointsPost(
        device_id="test_device",
        points=[point]
    )

    response = client.post(
        f"/api/public/tours/{tour_id}",
        headers={
            "X-API-KEY": apikey
        },
        json=pointspost.model_dump(mode="json")
    )
    return response
