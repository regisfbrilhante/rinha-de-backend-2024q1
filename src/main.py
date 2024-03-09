from fastapi import FastAPI
from src.schemas.schemas import Transacao
from src.repositorios.pgsql_connection_factory import create_connection

from src.repositorios.transacao_repositorio import TransacaoRepositorio


app = FastAPI()

connection = create_connection()
repositorio = TransacaoRepositorio(connection)


@app.post("/clientes/{cliente_id}/transacoes")
def criar_transacao(cliente_id: int, transacao: Transacao):
    response = repositorio.credito(cliente_id, transacao, 1000)
    return response


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
