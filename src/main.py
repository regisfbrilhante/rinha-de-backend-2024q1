from fastapi import FastAPI

from src.application.api.exception_handler import init_exception_handler
from src.repositorios.cliente_repositorio import ClienteRepositorio
from src.repositorios.pgsql_connection_factory import create_pool
from src.repositorios.transacao_repositorio import TransacaoRepositorio
from src.schemas.schemas import Transacao

app = FastAPI()
init_exception_handler(app)

pool = create_pool()
transacao_repositorio = TransacaoRepositorio(pool=pool)
cliente_repositorio = ClienteRepositorio(pool=pool)


@app.get("/")
def read_root():
    return {"version": "1.0.2"}


@app.post("/clientes/{cliente_id}/transacoes")
def criar_transacao(cliente_id: int, transacao: Transacao):
    if transacao.tipo == "d":
        return transacao_repositorio.debito(cliente_id, transacao)

    return transacao_repositorio.credito(cliente_id, transacao)


@app.get("/clientes/{cliente_id}/extrato")
def get_extrato(cliente_id: int):
    return cliente_repositorio.get_extrato(cliente_id)
