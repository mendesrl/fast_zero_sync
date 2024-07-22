from http import HTTPStatus

import pytest
from fastapi.exceptions import HTTPException
from jwt import decode

from fast_zero.security import (
    SECRET_KEY,
    create_access_token,
    get_current_user,
)


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert decoded['exp']  # Testa se o valor de exp foi adicionado ao token


def test_get_current_user(client, user, token):
    response = client.get(
        '/users/', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {'id': user.id, 'username': user.username, 'email': user.email}
        ]
    }


def test_get_username_not_found(client, user, token):
    response = client.get(
        f'/user/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_current_user_deve_dar_erro_de_jwt():
    with pytest.raises(HTTPException):
        get_current_user({'batata': 123})
