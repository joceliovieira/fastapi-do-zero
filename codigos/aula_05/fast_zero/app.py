from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import (
    Message,
    # UserDB,
    UserList,
    UsernameList,
    UserPublic,
    UserSchema,
)

app = FastAPI()


@app.post("/users/", response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    username_to_check = user.username
    email_to_check = user.email

    user_in_db = session.scalar(  # Scalar e nao sclars: Verifica pelo menos um
        select(User).where(
            (User.username == username_to_check) | (User.email == email_to_check)
        )
    )

    if user_in_db:
        if user_in_db.username == username_to_check:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail="username já existe.",
            )
        elif user_in_db.email == email_to_check:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="email já existe."
            )

    new_user = User(username=user.username, email=user.email, password=user.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    user_public = UserPublic(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
    )
    return user_public


@app.get("/users/", response_model=UserList)
def read_users(
    session: Session = Depends(get_session), skip: int = 0, limit: int = 100
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()

    return {"users": users}


@app.put("/users/{user_id}", response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    """Recebe user_id e user (modelo de usuario atualizado),
    retorna modelo UserPublic do usuario atualizado"""

    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado",
        )

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = user.password
    session.commit()  # Atualizar um dado do banco assim é massa demais! Zero SQL x_x
    session.refresh(db_user)

    return db_user


@app.delete("/users/{user_id}", response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.scalar(select(User).where(User.id == user_id))

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado",
        )

    session.delete(user)
    session.commit()

    return {"message": f"Usuário ID[{user_id}] deletado com sucesso."}


# Exercício - GET de recurso único
# Endpoint para obtenção de username únicos
@app.get("/users/unique_usernames", response_model=UsernameList)
def get_unique_username(session: Session = Depends(get_session)):
    usernames = session.scalars(select(User.username).distinct(User.username)).all()

    if len(usernames) == 0:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Não há usuários cadastrados."
        )

    return {"usernames": usernames}
