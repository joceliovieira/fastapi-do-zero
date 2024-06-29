from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import UserSchema, UserDB, UserList, UserPublic, Message

db = list()

app = FastAPI()


@app.post("/users/", response_model=UserPublic, status_code=HTTPStatus.CREATED)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(db) + 1, **user.model_dump())
    db.append(user_with_id)
    return user_with_id


@app.get("/users/", response_model=UserList)
def read_users():
    return {"users": db}


@app.put("/users/{user_id}", response_model=UserPublic)
def update_user(user: UserSchema, user_id: int):
    if user_id < 1 or user_id > len(db):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado --> ID inválido",
        )

    updated_user = UserDB(**user.model_dump(), id=user_id)
    db[user_id - 1] = updated_user

    return updated_user


@app.delete("/users/{user_id}", response_model=Message)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(db):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Usuário não encontrado --> ID inválido",
        )

    del db[user_id - 1]

    return {"message": f"Usuário ID[{user_id}] deletado com sucesso."}

