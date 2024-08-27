from http import HTTPStatus


# Exercício - teste prevendo falha com db vazio
def test_get_unique_username_empty(client):
    # Act
    response = client.get('/users/unique_usernames')

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_user_retorna_user(client):
    # Act
    response = client.post(
        url="/users/",
        json={"username": "kenan", "password": "kel", "email": "kenan@kel.com"}
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "email": "kenan@kel.com",
        "username": "kenan",
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
        json={
            "username": "chris",
            "email": "chris@market.com",
            "password": "water"
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "chris",
        "email": "chris@market.com",
        "id": 1,
    }


# Exercício - teste com db não-vazio
def test_get_unique_username(client):
    # Act
    response = client.get('/users/unique_usernames')
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'usernames': ['chris']}


def test_delete_users(client):
    # Arrange
    user_id = 1

    # Act
    response = client.delete(f'/users/{user_id}')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "message": f"Usuário ID[{user_id}] deletado com sucesso."
    }


# Exercício - Teste de atualização prevendo falha de ID inválido
def test_put_invalid_id(client):
    # Arrange
    user_id = -4

    # Act
    response = client.put(f'/users/{user_id}', json={
        'username': 'roger',
        'email': 'roger@kk.nick',
        'password': 'love'
    })

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND


# Exercício - Teste de delete prevendo falha de ID inválido
def test_delete_invalid_id(client):
    # Arrange
    user_id = -4

    # Act
    response = client.delete(f'/users/{user_id}')

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
