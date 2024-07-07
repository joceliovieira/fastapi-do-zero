from http import HTTPStatus
from fast_zero.schemas import UserPublic


# Teste de criação de usuario OK
def test_create_user_ok(client):
    # Act
    response = client.post(
        url="/users/",
        json={
            "username": "kenan",
            "password": "kel",
            "email": "kenan@kel.com",
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "kenan",
        "email": "kenan@kel.com",
    }


# Teste de criação de usuario com username já utilizado
def test_create_user_username_ja_utilizado(client, user):
    # Act
    response = client.post(
        url="/users/",
        json={
            "username": user.username,
            "password": "kel",
            "email": "kenan@kel.com",
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


# Teste de criação de usuario com username já utilizado
def test_create_user_email_ja_utilizado(client, user):
    # Act
    response = client.post(
        url="/users/",
        json={"username": "robinson", "password": "kel", "email": user.email},
    )

    # Assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


# Teste de consulta de usuarios SEM usuarios registrados
def test_get_users_empty(client):
    # Act
    response = client.get("/users/")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


# Teste de consulta de usuarios COM usuarios registrados
def test_get_users_not_empty(client, user):
    # Arrange
    # Valida o modelo de dados e retorna o mesmo objeto da entrada
    user = UserPublic.model_validate(user)
    # Transforma em um dicionário que vai ser comparado com o response da API
    user = user.model_dump()

    # Act
    response = client.get("/users/")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user]}


# Teste do GET /users/unique_usernames SEM usuários cadastrados
def test_get_unique_usernames_not_found(client):
    # Act
    response = client.get("/users/unique_usernames")

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND


# Teste do GET /users/unique_usernames COM usuários cadastrados
def test_get_unique_usernames_ok(client, user):
    # Act
    response = client.get("/users/unique_usernames")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"usernames": [user.username]}


# Teste de atualização de user
def test_update_user(client, user):
    # Act
    response = client.put(
        "/users/1",
        json={"username": "chris", "email": "chris@market.com", "password": "water"},
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "chris",
        "email": "chris@market.com",
        "id": 1,
    }


# Teste de delete user
def test_delete_users(client, user):
    # Arrange
    user_id = 1

    # Act
    response = client.delete(f"/users/{user_id}")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "message": f"Usuário ID[{user_id}] deletado com sucesso."
    }


# Teste considerando falha e a exceção que dever ser levantada
# em caso de ser passado um ID inválido
def test_put_invalid_id(client):
    # Arrange
    user_id = -4

    # Act
    response = client.put(
        f"/users/{user_id}",
        json={"username": "roger", "email": "roger@kk.nick", "password": "love"},
    )

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND


# Teste delete user com ID inválido
def test_delete_invalid_id(client):
    # Arrange
    user_id = -4

    # Act
    response = client.delete(f"/users/{user_id}")

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
