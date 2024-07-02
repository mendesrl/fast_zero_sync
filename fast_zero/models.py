# registry : Regista metadados que são os nomes dos campos
# (Nome da tabela, nome da coluna, tipo de dados, etc)
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


# uma classe de dados é uma classe que tem apenas campos de dados
@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    # Todas as vezes que for passar o objeto não precisa passar o ID
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str]
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
