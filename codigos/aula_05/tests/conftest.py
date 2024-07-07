import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from fast_zero.app import app
from fast_zero.models import table_registry, User
from fast_zero.database import get_session


# Sessão do banco - SQLAlchemy
@pytest.fixture()
def session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


# Cliente de testes - FastAPI
@pytest.fixture()
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = (
            get_session_override  # Substitui a sessão de produção pela de testes
        )
        yield client

    app.dependency_overrides.clear()

    return TestClient(app)


# Criação de usuário - SQLAlchemy
@pytest.fixture
def user(session):
    new_user = User(
        username="miles_davis_1984", email="milesdavis@music.org", password="jazz10"
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user
