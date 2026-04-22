import test_utils as util

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200, response.json()
    assert response.json() == {"message": "Hello World"}


def test_create_user(client):
    test_username = "test_user"
    test_password = "secret"
    response = util.create_test_user(client, test_username, test_password)
    assert response.status_code == 200, response.json()
    assert response.json()["username"] == test_username


def test_create_user_already_exist(client):
    test_username = "test_user"
    test_password = "secret"
    response = util.create_test_user(client, test_username, test_password)

    response = util.create_test_user(client, test_username, test_password)
    assert response.status_code == 409, response.json()
    assert response.json()["detail"] == "User already exists"


def test_token_generation(client):
    test_username = "test_user"
    test_password = "secret"
    response = util.create_test_user(client, test_username, test_password)
    assert response.status_code == 200, response.json()

    response = util.get_token(client, test_username, test_password)
    assert response.status_code == 200, response.json()

    data = response.json()
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_token_generation_incorrect_username_or_password(client):
    test_username = "test_user"
    test_password = "secret"
    response = util.create_test_user(client, test_username, test_password)
    assert response.status_code == 200, response.json()

    response = util.get_token(client, "user", test_password)
    assert response.status_code == 401, response.json()
    assert response.json()["detail"] == "Incorrect username or password" 

    response = util.get_token(client, test_username, "xxx")
    assert response.status_code == 401, response.json()
    assert response.json()["detail"] == "Incorrect username or password" 
