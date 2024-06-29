from http import HTTPStatus


def test_create_user_retorna_user(client):
    # Act
    response = client.post(
        url="/users/",
        json={"username": "kenan", "password": "kel", "email": "kenan@kel.com"},
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "email": "kenan@kel.com",
        "username": "kenan",
        "password": "kel",
        "id": 1,
    }


def test_get_users(client):
    # Act
    response = client.get("/users/")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [{"username": "kenan", "email": "kenan@kel.com", "id": 1}]
    }


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={"username": "chris", "email": "chris@market.com", "password": "water"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "chris",
        "email": "chris@market.com",
        "id": 1,
    }
