"""TP02 - Locadora de veiculos."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date


# ---------- Herança: Veiculo ----------
class Veiculo(ABC):
    def __init__(self, placa: str, modelo: str, ano: int, valor_diaria: float):
        self.placa, self.modelo, self.ano, self.valor_diaria = placa, modelo, ano, valor_diaria
        self.disponivel = True
        self._manutencoes: list[Manutencao] = []  # composicao

    @abstractmethod
    def taxa_extra(self) -> float: ...

    def calcular_aluguel(self, dias: int) -> float:
        return (self.valor_diaria + self.taxa_extra()) * dias

    def registrar_manutencao(self, data: date, tipo: str, custo: float) -> Manutencao:
        m = Manutencao(data, tipo, custo)  # o veiculo cria a manutencao
        self._manutencoes.append(m)
        return m

    @property
    def historico(self) -> tuple[Manutencao, ...]:
        return tuple(self._manutencoes)


class Carro(Veiculo):
    def taxa_extra(self) -> float:
        return 0.0


class Moto(Veiculo):
    def taxa_extra(self) -> float:
        return -10.0  # desconto


class Caminhao(Veiculo):
    def __init__(self, *a, capacidade_kg: float, **k):
        super().__init__(*a, **k)
        self.capacidade_kg = capacidade_kg

    def taxa_extra(self) -> float:
        return 80.0


class Manutencao:
    def __init__(self, data: date, tipo: str, custo: float):
        self.data, self.tipo, self.custo = data, tipo, custo

    def resumo(self) -> str:
        return f"{self.data:%d/%m/%Y} - {self.tipo}: R$ {self.custo:.2f}"


# ---------- Herança: Cliente ----------
class Cliente(ABC):
    def __init__(self, nome: str, documento: str, telefone: str):
        self.nome, self.documento, self.telefone = nome, documento, telefone

    @abstractmethod
    def tipo_documento(self) -> str: ...

    def contato(self) -> str:
        return f"{self.nome} ({self.tipo_documento()} {self.documento}) - {self.telefone}"


class PessoaFisica(Cliente):
    def tipo_documento(self) -> str:
        return "CPF"


class PessoaJuridica(Cliente):
    def tipo_documento(self) -> str:
        return "CNPJ"


# ---------- Condutor <>-- Contrato (composicao) ----------
class Condutor:
    def __init__(self, nome: str, cnh: str):
        self.nome, self.cnh = nome, cnh

    def habilitado(self) -> bool:
        return len(self.cnh) == 11


class Contrato:
    def __init__(self, cliente: Cliente, veiculo: Veiculo, inicio: date, fim_previsto: date,
                 nome_condutor: str, cnh: str):
        if not veiculo.disponivel:
            raise ValueError("Veiculo ja possui contrato ativo")
        self.cliente, self.veiculo = cliente, veiculo  # associacao
        self.inicio, self.fim_previsto = inicio, fim_previsto
        self.status = "ativo"
        self.condutor = Condutor(nome_condutor, cnh)  # composicao: criado pelo contrato
        self.valor_total = veiculo.calcular_aluguel((fim_previsto - inicio).days)
        veiculo.disponivel = False

    def finalizar(self) -> None:
        self.status = "finalizado"
        self.veiculo.disponivel = True

    def cancelar(self) -> None:
        self.status = "cancelado"
        self.veiculo.disponivel = True


if __name__ == "__main__":
    carro = Carro("ABC-1234", "Gol", 2022, 100.0)
    cli = PessoaFisica("Ana", "123.456.789-00", "8199999-0000")
    c = Contrato(cli, carro, date(2026, 10, 1), date(2026, 10, 4), "Ana", "12345678901")
    assert c.valor_total == 300.0 and not carro.disponivel
    try:
        Contrato(cli, carro, date(2026, 10, 2), date(2026, 10, 3), "Bia", "10987654321")
        raise SystemExit("deveria falhar")
    except ValueError:
        pass
    c.finalizar()
    assert carro.disponivel
    carro.registrar_manutencao(date(2026, 10, 5), "Troca de oleo", 150.0)
    print("TP02 ok:", carro.historico[0].resumo(), "|", c.condutor.nome)
