from datetime import datetime
from typing import List

from pydantic import BaseModel, field_validator


class Transacao(BaseModel):
    valor: int
    tipo: str
    descricao: str

    @field_validator("descricao")
    @classmethod
    def valida_descricao(cls, v):
        if len(v) > 10 or len(v) == 0:
            raise ValueError("A descrição deve conterno máximo 10 caracteres")
        return v

    @field_validator("tipo")
    @classmethod
    def valida_tipo(cls, v):
        if v not in ["c", "d"]:
            raise ValueError("Tipo de transação inválido")
        return v

    @field_validator("valor")
    @classmethod
    def valida_valor(cls, v):
        if v <= 0:
            raise ValueError("O valor da transação deve ser maior que zero")
        return v


class TransacaoRealizada(Transacao):
    realizada_em: datetime


class ResultadoTransacao(BaseModel):
    limite: int
    saldo: int


class Saldo(BaseModel):
    total: int
    data_extrato: datetime
    limite: int


class Extrato(BaseModel):
    saldo: Saldo
    ultimas_transacoes: List[TransacaoRealizada]
