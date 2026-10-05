"""Importa todos os models para que `Base.metadata` os conheça.

O Alembic (alembic/env.py) faz `import app.models`; sem isto o
`--autogenerate` não enxergaria as tabelas.
"""
from app.models.autor import Autor
from app.models.livro import Livro

__all__ = ["Autor", "Livro"]
