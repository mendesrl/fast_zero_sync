from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI()

DATABASE = []

# @app.get('/', status_code=HTTPStatus.OK, response_model=Message)
# def read_root():
#     return {'message': 'Hello, World!'}


# # Exercicio 1
# # - Crie um endpoint que retorna "olá mundo" usando HTML
# # - Escreva seu teste
# # - Dica: para capturar a resposta do HTML do cliente de testes,
# #   você pode usar response.text


# @app.get('/html', response_class=HTMLResponse)
# def read_html():
#     return """
#     <html>
#       <head>
#         <title> Nosso olá mundo!</title>
#       </head>
#       <body>
#         <h1> Olá Mundo </h1>
#       </body>
#     </html>
# """


# Recurso de user (manipular os dados de um usuario CRUD)


@app.post('/user/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(DATABASE) + 1)
    DATABASE.append(user_with_id)

    return user_with_id


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users():
    return {'users': DATABASE}


@app.put(
    '/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema):
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



# Exercícios
# Criar um endpoint de GET para pegar um único recurso como users/{id} e fazer seus testes.

@app.get('/user/{user_id}', response_model=UserPublic)
def read_user_id(user_id: int):
    if user_id > len(DATABASE) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='User not found :( ',
        )
    return DATABASE[user_id - 1]
