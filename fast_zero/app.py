from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

DATABASE = []


@app.get('/users/', response_model=UserList)
def read_users(
    limit: int = 1, offset: int = 0, session: Session = Depends(get_session)
):
    user = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': user}


# Exercícios
# Criar um endpoint de GET para pegar um
# único recurso como users/{id} e fazer seus testes.


@app.get('/user/{user_id}', response_model=UserPublic)
def read_user_id(user_id: int):
    if user_id > len(DATABASE) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found :( ',
        )
    return DATABASE[user_id - 1]


@app.post('/user/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.put(
    '/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session)):
    if user_id < 1 or user_id > len(DATABASE):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found :( ',
        )
    user_with_id = UserDB(**user.model_dump(), id=user_id)
    DATABASE[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/user/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(DATABASE) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found :( ',
        )
    del DATABASE[user_id - 1]
    return {'message': 'User deleted successfully!'}
