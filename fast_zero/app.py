from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Message, UserDB, UserPublic, UserSchema

app = FastAPI()

DATABASE = []


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello, World!'}


# Exercicio 1
# - Crie um endpoint que retorna "olá mundo" usando HTML
# - Escreva seu teste
# - Dica: para capturar a resposta do HTML do cliente de testes,
#   você pode usar response.text

@app.get('/html', response_class=HTMLResponse)
def read_html():
    return """
    <html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>
"""
