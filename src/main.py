from datetime import datetime
from typing import List, Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Transacao(BaseModel):
    valor: int
    tipo: str
    descricao: str


class TransacaoRealizada(Transacao):
    realizada_em: datetime


class Saldo(BaseModel):
    total: int
    data_extrato: datetime
    limite: int


class Extrato(BaseModel):
    saldo: Saldo
    ultimas_transacoes: List[TransacaoRealizada]


@app.post("/clientes/{cliente_id}/transacoes")
def criar_transacao(cliente_id: int, transacao: Transacao):
    return {"limite": 100000, "saldo": -9098}


@app.get("/clientes/{cliente_id}/extrato")
def get_extrato(cliente_id: int):
    return {
        "saldo": {
            "total": -9098,
            "data_extrato": "2024-01-17T02:34:41.217753Z",
            "limite": 100000,
        },
        "ultimas_transacoes": [
            {
                "valor": 10,
                "tipo": "c",
                "descricao": "descricao",
                "realizada_em": "2024-01-17T02:34:38.543030Z",
            },
            {
                "valor": 90000,
                "tipo": "d",
                "descricao": "descricao",
                "realizada_em": "2024-01-17T02:34:38.543030Z",
            },
        ],
    }
