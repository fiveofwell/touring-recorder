import test_utils as util

def test_rate_limit_root(client):
    # 1~10回
    for _ in range(10):
        response = client.get("/")
        assert response.status_code == 200, response.json()
    
    # 11回目はレートリミットに引っかかるはず
    response = client.get("/")
    assert response.status_code == 429, response.json()
    assert response.json()["detail"] == "Too many requests"


def test_rate_limit_token(client):
    test_username = "test_user"
    test_password = "secret"
    util.create_test_user(client, test_username, test_password)
    # 1回
    token = util.get_token(client, test_username, test_password).json()["access_token"]

    client.headers["Authorization"] = f"Bearer {token}"
    # 2~5回
    for _ in range(4):
        response = util.get_token(client, test_username, test_password)
        assert response.status_code == 200, response.json()
    
    # 6回目はレートリミットに引っかかるはず
    response = util.get_token(client, test_username, test_password)
    assert response.status_code == 429, response.json()
    assert response.json()["detail"] == "Too many requests"


def test_rate_limit_before_authentication(client):
    test_username = "test_user"
    test_password = "secret"

    # 1~5回
    for _ in range(5):
        response = util.get_token(client, test_username, test_password)
        assert response.status_code == 401, response.json()
    
    # 6回目はレートリミットに引っかかるはず
    response = util.get_token(client, test_username, test_password)
    assert response.status_code == 429, response.json()
    assert response.json()["detail"] == "Too many requests"


def test_rate_limit_internal(authenticated_client):
    # 1~100回
    for _ in range(100):
        response = authenticated_client.get("/api/internal/tours")
        assert response.status_code == 200, response.json()

    # 101回目はレートリミットに引っかかるはず
    response = authenticated_client.get("/api/internal/tours")
    assert response.status_code == 429, response.json()
    assert response.json()["detail"] == "Too many requests"


def test_rate_limit_public(device_client):
    tour_id = "test_tour"
    # 1~100回
    for _ in range(100):
        response = util.create_test_tour(device_client, tour_id)
        assert response.status_code == 200, response.json()

    # 101回目はレートリミットに引っかかるはず
    response = util.create_test_tour(device_client, tour_id)
    assert response.status_code == 429, response.json()
    assert response.json()["detail"] == "Too many requests"
