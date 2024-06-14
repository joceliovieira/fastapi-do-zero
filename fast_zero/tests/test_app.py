from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)  # Organizar - arrange

    response = client.get("/")  # Agir - act

    assert response.status_code == HTTPStatus.OK  # Verificar - assert

    assert response.json() == {"message": "Olá, planeta."}  # Verificar - assert
