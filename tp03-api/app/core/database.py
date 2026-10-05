"""Configuração do banco de dados (SQLAlchemy).

Este módulo centraliza tudo o que é "infraestrutura de banco":
- o engine (a conexão com o banco);
- a fábrica de sessões (SessionLocal);
- a classe Base, da qual todos os models herdam;
- a dependência `get_db`, usada nos routers via `Depends`.
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# SQLite em arquivo local: não precisa instalar nem configurar servidor.
# Para trocar de banco (ex.: PostgreSQL) basta mudar esta URL.
DATABASE_URL = "sqlite:///./biblioteca.db"

# `check_same_thread=False` é necessário no SQLite porque o FastAPI pode
# atender uma mesma requisição em threads diferentes.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


@event.listens_for(engine, "connect")
def _ativar_chaves_estrangeiras(dbapi_connection, _):
    """O SQLite ignora FOREIGN KEY por padrão; este PRAGMA liga a verificação."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# Cada requisição recebe a sua própria sessão. `autoflush=False` evita
# gravações implícitas: só vai ao banco quando chamamos `commit()`.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    """Classe base de todos os models. O Alembic lê `Base.metadata` para
    descobrir as tabelas ao gerar migrações."""


def get_db():
    """Dependência do FastAPI: abre uma sessão e garante que ela seja fechada.

    Uso em um endpoint:  `db: Session = Depends(get_db)`
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
