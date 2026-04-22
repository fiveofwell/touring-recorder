import test_utils as util

def test_register_device(authenticated_client):
    response =util.register_device(authenticated_client, "test_device")
    assert response.status_code == 200, response.json()
    assert response.json()["api_key"]

    response = authenticated_client.get("/api/internal/devices")
    assert response.status_code == 200, response.json()
    assert len(response.json()) == 1


def test_register_device_conflict(authenticated_client):
    util.register_device(authenticated_client, "test_device")
    response = util.register_device(authenticated_client, "test_device")
    assert response.status_code == 409, response.json()
    assert response.json()["detail"] == "Device already exists"

    response = authenticated_client.get("/api/internal/devices")
    assert response.status_code == 200, response.json()
    assert len(response.json()) == 1


def test_register_device_not_conflict(make_authenticated_client):
    client_a = make_authenticated_client("user1", "secret")
    client_b = make_authenticated_client("user2", "passW0rd")

    util.register_device(client_a, "test_device")

    response = util.register_device(client_b, "test_device")
    assert response.status_code == 200, response.json()

    response = client_a.get("/api/internal/devices")
    assert response.status_code == 200, response.json()
    assert len(response.json()) == 1

    response = client_b.get("/api/internal/devices")
    assert response.status_code == 200, response.json()
    assert len(response.json()) == 1


def test_delete_device(authenticated_client):
    response = util.register_device(authenticated_client, "test_device")
    device_id = response.json()["device_id"]

    response = authenticated_client.delete(f"/api/internal/devices/{device_id}")
    assert response.status_code == 204, response.json()

    response = authenticated_client.get("/api/internal/devices")
    assert response.status_code == 200, response.json()
    assert len(response.json()) == 0


def test_delete_device_other_user(make_authenticated_client):
    client_a = make_authenticated_client("user1", "secret")
    client_b = make_authenticated_client("user2", "passW0rd")

    device_id = util.register_device(client_a, "test_device").json()["device_id"]
    response = client_b.delete(f"/api/internal/devices/{device_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Device not found"


def test_delete_device_not_found(authenticated_client):
    response = authenticated_client.delete("/api/internal/devices/999999")
    assert response.status_code == 404, response.json()
    assert response.json()["detail"] == "Device not found"
