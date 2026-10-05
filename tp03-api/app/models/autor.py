"""Model `Autor` — tabela `autores`."""
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.livro import Livro


class Autor(Base):
    __tablename__ = "autores"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    nacionalidade: Mapped[str | None] = mapped_column(String(50), default=None)

    # Lado "um" da relação 1:N. `autor.livros` devolve a lista de livros do
    # autor. Sem cascade de delete de propósito: a API recusa (409) apagar um
    # autor que ainda tenha livros, em vez de apagá-los em silêncio.
    livros: Mapped[list["Livro"]] = relationship(back_populates="autor")
