from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app


@pytest.fixture()
def client():
    return TestClient(app)  # Arrange (Organizar/Preparar)


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act (Agir)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirme)
    assert response.json() == {'message': 'Hello, World!'}  # Assert (Afirme)


def test_read_html(client):
    response = client.get('/html')  # Act (Agir)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirme)
    assert (
        response.text
        == """
    <html>
      <head>
        <title> Nosso olá mundo!</title>
      </head>
      <body>
        <h1> Olá Mundo </h1>
      </body>
    </html>
"""
    )  # Assert (Afirme)

