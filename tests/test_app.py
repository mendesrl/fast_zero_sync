from http import HTTPStatus


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


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'larissa',
                'email': 'ribeiro@gmail.com',
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/user/1',
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
        'id': 1,
    }


def test_delete_user(client):
    response = client.delete('/user/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully!'}


# Exercícios
# Escrever um teste para o erro de 404 (NOT FOUND) para o endpoint de PUT;
# Escrever um teste para o erro de 404 (NOT FOUND) para o endpoint de DELETE;
# Criar um endpoint de GET para pegar um único recurso como users/{id}
# e fazer seus testes.


def test_update_user_not_found(client):
    response = client.put(
        '/user/2',
        json={
            'username': 'bob',
            'email': 'lala@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found :( '}


def test_delete_user_not_found(client):
    response = client.delete('/user/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found :( '}


def test_read_user_id(client):
    response = client.post(
        '/user/',
        json={
            'username': 'larissa',
            'email': 'ribeiro@gmail.com',
            'password': '123456',
        },
    )  # Act (Agir)
    response = client.get('/user/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'larissa',
        'email': 'ribeiro@gmail.com',
    }


def test_read_user_id_not_found(client):
    response = client.get('/user/2')
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found :( '}
