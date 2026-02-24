import uuid
from tests.test_utils import create_test_tour, create_invalid_test_tour, create_test_tour_with_apikey
from schemas.api_schema import TourUpdate
import settings

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_get_tours(client):
    response = client.get("/api/internal/tours")
    assert response.status_code == 200


def test_get_tours_detail(client):
    create_test_tour(client, str(uuid.uuid4()))
    create_test_tour(client, str(uuid.uuid4()))
    create_test_tour(client, str(uuid.uuid4()))

    response = client.get("/api/internal/tours")
    tours = response.json()

    for tour in tours:
        tour_id = tour["tour_id"]
        tour_response = client.get(f"/api/internal/tours/{tour_id}")
        assert tour_response.status_code == 200
        assert len(tour_response.json()["points"]) == 1


def test_get_tour_not_found(client):
    tour_id = str(uuid.uuid4())
    response = client.get(f"/api/internal/tours/{tour_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Tour not found"


def test_post_points(client):
    tour_id = str(uuid.uuid4())
    response = create_test_tour(client, tour_id)
    assert response.status_code == 200
    assert response.json() == {"ok": True}

    response = client.get(f"/api/internal/tours/{tour_id}")
    assert response.status_code == 200
    assert len(response.json()["points"]) == 1


def test_post_invalid_points(client):
    tour_id = str(uuid.uuid4())
    response = create_invalid_test_tour(client, tour_id)
    assert response.status_code == 422

    response = client.get(f"/api/internal/tours/{tour_id}")
    assert response.status_code == 404


def test_delete_tour(client):
    tour_id = str(uuid.uuid4())
    create_test_tour(client, tour_id)
    response = client.delete(f"/api/internal/tours/{tour_id}")
    assert response.status_code == 204

    response = client.get(f"/api/internal/tours/{tour_id}")
    assert response.status_code == 404 


def test_delete_tour_not_found(client):
    tour_id = str(uuid.uuid4())
    response = client.delete(f"/api/internal/tours/{tour_id}")
    assert response.status_code == 404


def test_public_post(client):
    tour_id = str(uuid.uuid4())
    response = create_test_tour_with_apikey(client, tour_id, settings.X_API_KEY)
    assert response.status_code == 200

    response = client.get(f"/api/internal/tours/{tour_id}")
    assert response.status_code == 200
    assert len(response.json()["points"]) == 1


def test_public_post_invalid_apikey(client):
    tour_id = str(uuid.uuid4())
    response = create_test_tour_with_apikey(client, tour_id, str(uuid.uuid4()))
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

    response = client.get(f"/api/internal/tours/{tour_id}")
    assert response.status_code == 404 


def test_tour_name_change(client):
    tour_id = str(uuid.uuid4())
    create_test_tour(client, tour_id)

    tour_name = str(uuid.uuid4())
    body = TourUpdate(
            tour_name = tour_name
    )

    response = client.patch(f"/api/internal/tours/{tour_id}", json=body.model_dump(mode="json"))
    assert response.status_code == 200
    assert response.json()["tour_name"] == tour_name
