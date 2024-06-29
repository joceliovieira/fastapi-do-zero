from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.hello_world import app


def test_root_deve_retornar_ok_e_ola_mundo():
    # Organizar - arrange
    client = TestClient(app)

    # Agir - act
    response = client.get("/")

    # Verificar - assert
    assert response.status_code == HTTPStatus.OK

    # Verificar - assert
    assert response.json() == {"message": "Olá, planeta."}


def test_hw_html_deve_retornar_ok_e_html():
    # Organizar - arrange
    client = TestClient(app)

    # Organizar - arrange
    response_text = """
  <html>
    <head>
      <title> Nosso olá mundo!</title>
    </head>
    <body>
      <h1> Olá Mundo </h1>
    </body>
  </html>"""

    # Agir - act
    response = client.get("/hw_html")

    # Verificar - Status code
    assert response.status_code == HTTPStatus.OK

    # Verificar - Message text
    assert response.text == response_text
