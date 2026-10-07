"""Router de Autores — CRUD de `/autores`.

O prefixo `/autores` é definido no `main.py`, por isso as rotas aqui são só
`/` e `/{autor_id}`.
"""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Autor
from app.schemas.autor import AutorCreate, AutorResponse, AutorUpdate

router = APIRouter()


def _buscar_autor(db: Session, autor_id: int) -> Autor:
    """Devolve o autor ou responde 404."""
    autor = db.get(Autor, autor_id)
    if autor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Autor {autor_id} não encontrado.",
        )
    return autor


@router.post("/", response_model=AutorResponse, status_code=status.HTTP_201_CREATED)
def criar_autor(dados: AutorCreate, db: Session = Depends(get_db)):
    autor = Autor(**dados.model_dump())
    db.add(autor)
    db.commit()
    db.refresh(autor)
    return autor


@router.get("/", response_model=list[AutorResponse])
def listar_autores(db: Session = Depends(get_db)):
    return db.scalars(select(Autor).order_by(Autor.id)).all()


@router.get("/{autor_id}", response_model=AutorResponse)
def buscar_autor(autor_id: int, db: Session = Depends(get_db)):
    return _buscar_autor(db, autor_id)


@router.patch("/{autor_id}", response_model=AutorResponse)
def atualizar_autor(autor_id: int, dados: AutorUpdate, db: Session = Depends(get_db)):
    autor = _buscar_autor(db, autor_id)
    # `exclude_unset=True`: só os campos que o cliente realmente enviou.
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(autor, campo, valor)
    db.commit()
    db.refresh(autor)
    return autor


@router.delete("/{autor_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_autor(autor_id: int, db: Session = Depends(get_db)):
    autor = _buscar_autor(db, autor_id)
    # Regra de negócio: não apagar um autor que ainda tem livros. Responder
    # 409 é mais claro do que apagar os livros junto ou deixar o banco falhar.
    if autor.livros:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=(
                f"Autor {autor_id} ainda tem {len(autor.livros)} livro(s) cadastrado(s). "
                "Remova os livros antes de apagar o autor."
            ),
        )
    db.delete(autor)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
