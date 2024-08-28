from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import Select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import (
    Message,
    UserList,
    UsernameList,
    UserPublic,
    UserSchema,
)

app = FastAPI()
db = list()


@app.post('/users/', response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    # Busca por usuários com condição não permitida
    # Condição: user/email devem ser unicos
    user_in_db = session.scalar(
        Select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    print('user_in_db')
    print(user_in_db)

    # Checa se o usuário já existe no bd
    if user_in_db:
        if user_in_db.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Usuário já existe'
            )
        if user_in_db.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail='Usuário já existe'
            )
    # Equivalente a else:
    db_user = User(**user.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def read_users(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    users = session.scalars(Select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(
    user: UserSchema, user_id: int, session: Session = Depends(get_session)
):
    # Verifica se o usuário existe
    db_user = session.scalar(Select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado --> ID inválido',
        )

    db_user.username = user.username
    db_user.password = user.password
    db_user.email = user.email

    session.commit()
    session.refresh(db_user)
    return db_user


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    # Verifica se o usuário existe
    db_user = session.scalar(Select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Usuário não encontrado --> ID inválido',
        )

    session.delete(db_user)
    session.commit()

    return {'message': f'Usuário ID[{user_id}] deletado com sucesso.'}


# Exercício - GET de recurso único
# Endpoint para obtenção de username únicos
@app.get('/users/unique_usernames', response_model=UsernameList)
def get_unique_username(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session),
):
    # Verifica se existe(m) usuário(s)
    db_users = session.scalars(Select(User).offset(skip).limit(limit)).unique().all()  # noqa: E501

    print()
    print('db_usersdb_usersdb_usersdb_users')
    print(db_users)
    if len(db_users) == 0:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Não existem usuários cadastrados',
        )

    unique_usernames = [user.username for user in db_users]

    return {'usernames': unique_usernames}
