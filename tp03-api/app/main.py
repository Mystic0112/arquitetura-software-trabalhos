"""Ponto de entrada da API da Biblioteca.

Rodar:  uvicorn app.main:app --reload      (docs em http://localhost:8000/docs)

Obs.: as tabelas NÃO são criadas aqui. O banco é criado exclusivamente via
migrações do Alembic (`alembic upgrade head`), como exige o trabalho.
"""
from fastapi import FastAPI

from app.routers import autores, livros

app = FastAPI(
    title="API da Biblioteca",
    description="TP03 de Arquitetura de Software: Autores e Livros (FastAPI + SQLAlchemy + Alembic).",
)

# Cada recurso tem seu próprio router; o prefixo e a tag organizam o Swagger.
app.include_router(autores.router, prefix="/autores", tags=["autores"])
app.include_router(livros.router, prefix="/livros", tags=["livros"])
