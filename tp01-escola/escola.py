"""TP01 - Sistema de escola.

Relacionamentos:
- Escola <>-- Sala        : COMPOSICAO  (Escola cria as salas; sem escola, sem salas)
- Escola  --  Professor   : ASSOCIACAO N:N (existem de forma independente)
- Aluno  <>-- Endereco    : AGREGACAO   (nasce com o aluno, mas sobrevive a ele)
"""
from __future__ import annotations


class Endereco:
    def __init__(self, rua: str, numero: str, cidade: str, cep: str):
        self.rua, self.numero, self.cidade, self.cep = rua, numero, cidade, cep

    def formatar(self) -> str:
        return f"{self.rua}, {self.numero} - {self.cidade} ({self.cep})"


class Aluno:
    def __init__(self, nome: str, matricula: str, endereco: Endereco):
        self.nome, self.matricula = nome, matricula
        self.endereco: Endereco | None = endereco

    def mudar_endereco(self, novo: Endereco) -> None:
        self.endereco = novo

    def remover(self) -> Endereco | None:
        """Remove o aluno; o endereco continua existindo e e devolvido (ex: relatorios)."""
        endereco, self.endereco = self.endereco, None
        return endereco


class Sala:
    def __init__(self, numero: int, capacidade: int):
        self.numero, self.capacidade = numero, capacidade

    def comporta(self, quantidade: int) -> bool:
        return quantidade <= self.capacidade


class Professor:
    def __init__(self, nome: str, disciplina: str, cpf: str):
        self.nome, self.disciplina, self.cpf = nome, disciplina, cpf
        self.escolas: list[Escola] = []

    def lecionar_em(self, escola: Escola) -> None:
        escola.contratar(self)


class Escola:
    def __init__(self, nome: str, cnpj: str):
        self.nome, self.cnpj = nome, cnpj
        self._salas: list[Sala] = []  # composicao: ciclo de vida preso a escola
        self.professores: list[Professor] = []
        self.alunos: list[Aluno] = []

    def criar_sala(self, numero: int, capacidade: int) -> Sala:
        sala = Sala(numero, capacidade)  # a escola instancia a sala
        self._salas.append(sala)
        return sala

    @property
    def salas(self) -> tuple[Sala, ...]:
        return tuple(self._salas)

    def contratar(self, professor: Professor) -> None:
        if professor not in self.professores:
            self.professores.append(professor)
            professor.escolas.append(self)

    def matricular(self, aluno: Aluno) -> None:
        self.alunos.append(aluno)

    def fechar(self) -> None:
        self._salas.clear()  # salas deixam de existir
        for p in self.professores:
            p.escolas.remove(self)  # professores continuam existindo
        self.professores.clear()


if __name__ == "__main__":
    escola = Escola("Escola Central", "12.345.678/0001-90")
    escola.criar_sala(101, 30)
    prof = Professor("Maria", "Matematica", "111.222.333-44")
    outra = Escola("Escola Norte", "98.765.432/0001-10")
    prof.lecionar_em(escola)
    prof.lecionar_em(outra)
    aluno = Aluno("Joao", "2026001", Endereco("Rua A", "10", "Recife", "50000-000"))
    escola.matricular(aluno)

    escola.fechar()
    assert escola.salas == ()          # composicao: salas morrem com a escola
    assert prof.escolas == [outra]     # professor sobrevive e segue na outra escola
    end = aluno.remover()
    assert end is not None             # endereco sobrevive ao aluno
    print("TP01 ok:", end.formatar())
