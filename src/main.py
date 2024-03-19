from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.application.api.exception_handler import init_exception_handler
from src.repositorios.cliente_repositorio import ClienteRepositorio
from src.repositorios.pgsql_connection_factory import create_pool
from src.repositorios.transacao_repositorio import TransacaoRepositorio
from src.schemas.schemas import Transacao


@asynccontextmanager
async def lifespan(app: FastAPI):
    pool = await create_pool()
    transacao_repositorio = TransacaoRepositorio(pool=pool)
    cliente_repositorio = ClienteRepositorio(pool=pool)

    app.transacao_repositorio = transacao_repositorio
    app.cliente_repositorio = cliente_repositorio
    yield


app = FastAPI(lifespan=lifespan)

init_exception_handler(app)


@app.post("/clientes/{cliente_id}/transacoes")
async def criar_transacao(cliente_id: int, transacao: Transacao):
    if transacao.tipo == "d":
        return await app.transacao_repositorio.debito(cliente_id, transacao)

    return await app.transacao_repositorio.credito(cliente_id, transacao)


@app.get("/clientes/{cliente_id}/extrato")
async def get_extrato(cliente_id: int):
    return await app.cliente_repositorio.get_extrato(cliente_id)
