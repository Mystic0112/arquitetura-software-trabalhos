"""Schemas Pydantic de `Autor`.

Cada operação tem o seu schema:
- `AutorCreate`: o que o cliente envia para criar (POST);
- `AutorUpdate`: o que o cliente envia para atualizar (PATCH), tudo opcional;
- `AutorResponse`: o que a API devolve.
"""
from pydantic import BaseModel, ConfigDict, field_validator


class AutorCreate(BaseModel):
    nome: str
    nacionalidade: str | None = None


class AutorUpdate(BaseModel):
    nome: str | None = None
    nacionalidade: str | None = None

    @field_validator("nome")
    @classmethod
    def nao_aceita_nulo(cls, valor):
        """O nome pode ser omitido, mas não enviado como `null`: no banco ele
        é obrigatório. Omitir = não mexer; `null` = erro 422."""
        if valor is None:
            raise ValueError("não pode ser nulo")
        return valor


class AutorResponse(BaseModel):
    # Permite montar a resposta direto a partir do model do SQLAlchemy.
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    nacionalidade: str | None
