import test_utils as util

def test_get_user(client):
    test_username = "test_user"
    test_password = "secret"

    util.create_test_user(client, test_username, test_password)
    token = util.get_token(client, test_username, test_password).json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"
    response = client.get("/api/internal/users/me")

    assert response.status_code == 200, response.json()
    assert response.json()["username"] == "test_user"


def test_get_user_invalid_token(client):
    test_username = "test_user"
    test_password = "secret"

    util.create_test_user(client, test_username, test_password)
    token = util.get_token(client, test_username, test_password).json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}xxx"
    response = client.get("/api/internal/users/me")

    assert response.status_code == 401, response.json()
    assert response.json()["detail"] == "Could not validate credentials"
