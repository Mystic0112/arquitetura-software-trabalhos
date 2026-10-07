"""Router de Livros — CRUD de `/livros`.

O prefixo `/livros` é definido no `main.py`, por isso as rotas aqui são só
`/` e `/{livro_id}`.
"""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Autor, Livro
from app.schemas.livro import LivroCreate, LivroResponse, LivroUpdate

router = APIRouter()


def _buscar_livro(db: Session, livro_id: int) -> Livro:
    """Devolve o livro ou responde 404."""
    livro = db.get(Livro, livro_id)
    if livro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Livro {livro_id} não encontrado.",
        )
    return livro


def _validar_autor(db: Session, autor_id: int) -> None:
    """Valida a chave estrangeira: o autor precisa existir antes de ser
    associado a um livro. Responde 404 com mensagem clara se não existir."""
    if db.get(Autor, autor_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Autor {autor_id} não encontrado. Cadastre o autor antes do livro.",
        )


@router.post("/", response_model=LivroResponse, status_code=status.HTTP_201_CREATED)
def criar_livro(dados: LivroCreate, db: Session = Depends(get_db)):
    _validar_autor(db, dados.autor_id)
    livro = Livro(**dados.model_dump())
    db.add(livro)
    db.commit()
    db.refresh(livro)
    return livro


@router.get("/", response_model=list[LivroResponse])
def listar_livros(autor_id: int | None = None, db: Session = Depends(get_db)):
    """Lista todos os livros. Use `?autor_id=` para filtrar por autor."""
    consulta = select(Livro).order_by(Livro.id)
    if autor_id is not None:
        consulta = consulta.where(Livro.autor_id == autor_id)
    return db.scalars(consulta).all()


@router.get("/{livro_id}", response_model=LivroResponse)
def buscar_livro(livro_id: int, db: Session = Depends(get_db)):
    return _buscar_livro(db, livro_id)


@router.patch("/{livro_id}", response_model=LivroResponse)
def atualizar_livro(livro_id: int, dados: LivroUpdate, db: Session = Depends(get_db)):
    livro = _buscar_livro(db, livro_id)
    # `exclude_unset=True`: só os campos que o cliente realmente enviou.
    alteracoes = dados.model_dump(exclude_unset=True)
    if "autor_id" in alteracoes:
        _validar_autor(db, alteracoes["autor_id"])
    for campo, valor in alteracoes.items():
        setattr(livro, campo, valor)
    db.commit()
    db.refresh(livro)
    return livro


@router.delete("/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = _buscar_livro(db, livro_id)
    db.delete(livro)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
