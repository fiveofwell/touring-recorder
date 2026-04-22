import uuid
import test_utils as util
from schemas.api_schema import TourUpdate

def test_get_tours(authenticated_client):
    response = authenticated_client.get(f"/api/internal/tours")
    assert response.status_code == 200 , response.json()


def test_delete_tour(authenticated_client):
    tour_id = str(uuid.uuid4())
    util.create_test_tour(authenticated_client, tour_id)
    response = authenticated_client.delete(f"/api/internal/tours/{tour_id}")
    assert response.status_code == 204, response.json()

    response = authenticated_client.get(f"/api/internal/tours/{tour_id}/points")
    assert response.status_code == 404 , response.json()
    assert response.json()["detail"] == "Tour not found"


def test_delete_tour_other_user(make_authenticated_client):
    client_a = make_authenticated_client("user1", "secret")
    client_b = make_authenticated_client("user2", "passW0rd")

    tour_id = str(uuid.uuid4())
    util.create_test_tour(client_a, tour_id)

    response = client_b.delete(f"/api/internal/tours/{tour_id}")
    assert response.status_code == 404, response.json()
    assert response.json()["detail"] == "Tour not found"


def test_delete_tour_not_found(authenticated_client):
    tour_id = str(uuid.uuid4())
    response = authenticated_client.delete(f"/api/internal/tours/{tour_id}")
    assert response.status_code == 404, response.json()
    assert response.json()["detail"] == "Tour not found"


def test_tour_name_change(authenticated_client):
    tour_id = str(uuid.uuid4())
    util.create_test_tour(authenticated_client, tour_id)

    tour_name = str(uuid.uuid4())
    body = TourUpdate(
        tour_name=tour_name
    )

    response = authenticated_client.patch(f"/api/internal/tours/{tour_id}", json=body.model_dump(mode="json"))
    assert response.status_code == 200, response.json()
    assert response.json()["tour_name"] == tour_name


def test_tour_name_change_not_found(authenticated_client):
    tour_id = str(uuid.uuid4())
    util.create_test_tour(authenticated_client, tour_id)

    tour_name = str(uuid.uuid4())
    body = TourUpdate(
        tour_name=tour_name
    )

    tour_id = str(uuid.uuid4())
    response = authenticated_client.patch(f"/api/internal/tours/{tour_id}", json=body.model_dump(mode="json"))
    assert response.status_code == 404, response.json()
    assert response.json()["detail"] == "Tour not found"


def test_tour_name_change_other_user(make_authenticated_client):
    client_a = make_authenticated_client("user1", "secret")
    client_b = make_authenticated_client("user2", "passW0rd")

    tour_id = str(uuid.uuid4())
    util.create_test_tour(client_a, tour_id)

    tour_name = str(uuid.uuid4())
    body = TourUpdate(
        tour_name=tour_name
    )

    response = client_b.patch(f"/api/internal/tours/{tour_id}", json=body.model_dump(mode="json"))
    assert response.status_code == 404, response.json()
    assert response.json()["detail"] == "Tour not found"
