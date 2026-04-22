import uuid
import test_utils as util

def test_post_points(authenticated_client):
    tour_id = str(uuid.uuid4())
    response = util.create_test_tour(authenticated_client, tour_id)
    assert response.status_code == 200, response.json()
    assert response.json() == {"ok": True}


def test_post_points_duplication(authenticated_client):
    tour_id = str(uuid.uuid4())
    response = util.create_test_tour(authenticated_client, tour_id)
    assert response.status_code == 200, response.json()
    assert response.json() == {"ok": True}

    # 重複してデータが送られた想定
    response = util.create_test_tour(authenticated_client, tour_id)
    assert response.status_code == 200, response.json()
    assert response.json() == {"ok": True}

    response = authenticated_client.get(f"/api/internal/tours/{tour_id}/points")
    assert response.status_code == 200, response.json()
    assert len(response.json()["points"]) == 1


def test_post_points_other_user(make_authenticated_client):
    client_a = make_authenticated_client("user1", "secret")
    client_b = make_authenticated_client("user2", "passw0rd")

    tour_id = str(uuid.uuid4())
    util.create_test_tour(client_a, tour_id)

    response = util.create_test_tour(client_b, tour_id)
    assert response.status_code == 404, response.json()


def test_get_points(authenticated_client):
    tour_id = str(uuid.uuid4())
    response = util.create_test_tour(authenticated_client, tour_id)

    response = authenticated_client.get(f"/api/internal/tours/{tour_id}/points")
    assert response.status_code == 200, response.json()


def test_get_points_other_user(make_authenticated_client):
    client_a = make_authenticated_client("user1", "secret")
    client_b = make_authenticated_client("user2", "passw0rd")

    tour_id = str(uuid.uuid4())
    response = util.create_test_tour(client_a, tour_id)

    response = client_b.get(f"/api/internal/tours/{tour_id}/points")
    assert response.status_code == 404, response.json()
    assert response.json()["detail"] == "Tour not found"


def test_get_points_not_found(authenticated_client):
    tour_id = str(uuid.uuid4())
    response = authenticated_client.get(f"/api/internal/tours/{tour_id}/points")
    assert response.status_code == 404, response.json()
    assert response.json()["detail"] == "Tour not found"

