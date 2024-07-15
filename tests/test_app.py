from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/user/',
        json={
            'username': 'larissa',
            'email': 'ribeiro@gmail.com',
            'password': '123456',
        },
    )  # Act (Agir)

    assert response.status_code == HTTPStatus.CREATED  # Assert (Afirme)
    assert response.json() == {
        'id': 1,
        'username': 'larissa',
        'email': 'ribeiro@gmail.com',
    }


def test_create_user_with_existing_username(client, user):
    response = client.post(
        '/user/',
        json={
            'username': user.username,
            'email': user.email,
            'password': '123456',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_create_user_with_existing_email(client, user):
    response = client.post(
        '/user/',
        json={
            'username': 'larissa',
            'email': user.email,
            'password': '123456',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_list_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': user.id,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/user/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_update_user_not_found(client, user, token):
    response = client.put(
        f'/users/{user.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'lala@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'Not enough permissions to update this user'
    }


def test_delete_user_not_found(client, user, token):
    response = client.delete(
        f'/user/{user.id + 1}', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {
        'detail': 'Not enough permissions to update this user'
    }


def test_read_user_id(client, user):
    response = client.post(
        '/user/',
        json={
            'username': 'larissa',
            'email': 'ribeiro@gmail.com',
            'password': '123456',
        },
    )
    response = client.get('/user/2')
    assert response.json() == {
        'id': 2,
        'username': 'larissa',
        'email': 'ribeiro@gmail.com',
    }


def test_read_user_id_not_found(client, user):
    response = client.get('/user/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.username, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_invalid(client, user):
    response = client.post(
        '/token',
        data={'username': user.username, 'password': 'wrongpassword'},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_get_token_invalid_username(client, user):
    response = client.post(
        '/token',
        data={'username': 'wrong', 'password': user.clean_password},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect username or password'}
