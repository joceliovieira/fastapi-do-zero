from http import HTTPStatus


def test_create_user_ok(client):
    # Act
    response = client.post(
        url='/users/',
        json={
            'username': 'kenan',
            'password': 'kel',
            'email': 'kenan@kel.com',
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'email': 'kenan@kel.com',
        'username': 'kenan',
        'id': 1,
    }


def test_create_user_username_existente(client, user):
    # Act
    response = client.post(
        url='/users/',
        json={
            'username': 'teste',
            'password': 'kel',
            'email': 'kenan@kel.com',
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Usuário já existe'


def test_create_user_email_existente(client, user):
    # Act
    response = client.post(
        url='/users/',
        json={
            'username': 'kenan',
            'password': 'kel',
            'email': 'teste@test.com',
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Usuário já existe'


def test_get_users_bd_vazio(client):
    # Act
    response = client.get('/users/')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_get_users_ok(client, user):
    # Act
    response = client.get('/users/')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [{'username': 'teste', 'email': 'teste@test.com', 'id': 1}]
    }
    # Outra forma de extrair os dados do user e verificar
    # user_schema = UserPublic.model_validate(user).model_dump()
    # assert response.json() == {'users': [user_schema]}


def test_update_user_ok(client, user):
    # Act
    response = client.put(
        '/users/1',
        json={
            'username': 'chris',
            'password': 'senha',
            'email': 'chris@market.com',
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'chris',
        'email': 'chris@market.com',
    }


def test_update_user_db_vazio(client):
    # Act
    response = client.put(
        '/users/1',
        json={
            'username': 'chris',
            'password': 'senha',
            'email': 'chris@market.com',
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    msg = 'Usuário não encontrado --> ID inválido'
    assert response.json()['detail'] == msg


def test_delete_users_db_vazio(client):
    # Arrange
    user_id = 1

    # Act
    response = client.delete(f'/users/{user_id}')

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    msg = 'Usuário não encontrado --> ID inválido'
    assert response.json()['detail'] == msg


def test_delete_users_ok(client, user):
    # Arrange
    user_id = 1

    # Act
    response = client.delete(f'/users/{user_id}')

    # Assert
    assert response.status_code == HTTPStatus.OK
    msg = {'message': f'Usuário ID[{user_id}] deletado com sucesso.'}
    assert response.json() == msg


# Exercício - teste com db não-vazio
def test_get_unique_username_ok(client, user):
    # Act
    response = client.get('/users/unique_usernames')
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'usernames': ['teste']}


# Exercício - teste prevendo falha com db vazio
def test_get_unique_username_empty(client):
    # Act
    response = client.get('/users/unique_usernames')
    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    msg = {'detail': 'Não existem usuários cadastrados'}
    assert response.json() == msg


# Exercício - Teste de atualização prevendo falha de ID inválido
def test_put_invalid_id(client):
    # Arrange
    user_id = -4

    # Act
    response = client.put(
        f'/users/{user_id}',
        json={
            'username': 'roger',
            'email': 'roger@kk.nick',
            'password': 'love',
        },
    )

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
