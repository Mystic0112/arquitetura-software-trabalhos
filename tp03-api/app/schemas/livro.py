"""Schemas Pydantic de `Livro`.

Cada operação tem o seu schema:
- `LivroCreate`: o que o cliente envia para criar (POST);
- `LivroUpdate`: o que o cliente envia para atualizar (PATCH), tudo opcional;
- `LivroResponse`: o que a API devolve.
"""
from pydantic import BaseModel, ConfigDict, field_validator


class LivroCreate(BaseModel):
    titulo: str
    ano: int | None = None
    autor_id: int


class LivroUpdate(BaseModel):
    titulo: str | None = None
    ano: int | None = None
    autor_id: int | None = None

    @field_validator("titulo", "autor_id")
    @classmethod
    def nao_aceita_nulo(cls, valor):
        """Os campos podem ser omitidos, mas não enviados como `null`: no banco
        eles são obrigatórios. Omitir = não mexer; `null` = erro 422."""
        if valor is None:
            raise ValueError("não pode ser nulo")
        return valor


class LivroResponse(BaseModel):
    # Permite montar a resposta direto a partir do model do SQLAlchemy.
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    ano: int | None
    autor_id: int
