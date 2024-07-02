# Para criar uma conexão com o banco de dados
from sqlalchemy import select

from fast_zero.models import User

# def test_create_user():
#     # criar um database do sqlite
#     # unico que cria um arquivo database.db
#     # por isso a escolha do SQLite

#     # Conexão real
#     # engine = create_engine('sqlite:///database.db')

#     # Conexão em memória
#     engine = create_engine('sqlite:///:memory:')

#     table_registry.metadata.create_all(engine)

#     with Session(engine) as session:
#         user = User(
#             username='alic',
#             password='secre',
#             email='test@test',
#         )
#         session.add(user)
#         session.commit()
#         # session.refresh(user)

#         # Retorna o registro do banco de dados
#         #  do objeto python
#         result = session.scalar(
#           select(User).where(
#           User.email == 'test@test'))

#     assert user.username == 'alic'
#     assert result.email == 'test@test'


def test_create_user(session):
    user = User(
        username='alice',
        password='secret',
        email='test@test.com',
    )

    session.add(user)
    session.commit()

    result = session.scalar(select(User).where(User.email == 'test@test.com'))

    assert user.username == 'alice'
    assert result.email == 'test@test.com'
