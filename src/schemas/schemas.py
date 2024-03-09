from datetime import datetime
from typing import List

from pydantic import BaseModel


class Transacao(BaseModel):
    valor: int
    tipo: str
    descricao: str


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
