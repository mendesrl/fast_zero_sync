from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)  # Arrange (Organizar/Preparar)

    response = client.get('/laris')  # Act (Agir)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirme)
    assert response.json() == {'message': 'Hello, World!'}  # Assert (Afirme)
