import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.models import table_registry


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    # Cria uma sessão com uma instancia sqlite em memoria para testes
    engine = create_engine('sqlite:///:memory:')

    # Cria as tabelas no banco de testes
    table_registry.metadata.create_all(engine)

    # Injeta a sessão toda vez que for chamada a fixture
    with Session(engine) as session:
        yield session

    # Dropa todas as tabelas da instância do banco de testes após finalizar
    # o teste que o chamou
    table_registry.metadata.drop_all(engine)
