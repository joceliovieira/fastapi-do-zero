import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import User, table_registry


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    # Cria uma sessão com uma instancia sqlite em memoria para testes
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    # Cria as tabelas no banco de testes
    table_registry.metadata.create_all(engine)

    # Injeta a sessão toda vez que for chamada a fixture
    with Session(engine) as session:
        yield session

    # Dropa todas as tabelas da instância do banco de testes após finalizar
    # o teste que o chamou
    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session):
    user = User(username='teste', email='teste@test.com', password='testtest')
    session.add(user)
    session.commit()
    session.refresh(user)

    return user
