"""Model `Livro` — tabela `livros`."""
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.autor import Autor


class Livro(Base):
    __tablename__ = "livros"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(150))
    ano: Mapped[int | None] = mapped_column(default=None)

    # Chave estrangeira: cada livro pertence a exatamente um autor.
    autor_id: Mapped[int] = mapped_column(ForeignKey("autores.id"))

    # Lado "muitos" da relação. `livro.autor` devolve o objeto Autor.
    autor: Mapped["Autor"] = relationship(back_populates="livros")
