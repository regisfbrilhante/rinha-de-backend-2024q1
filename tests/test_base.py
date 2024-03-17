import os

import pytest
import pytest_asyncio

from src.repositorios.pgsql_connection_factory import create_pool
from src.repositorios.transacao_repositorio import TransacaoRepositorio


class TestBase:

    @pytest_asyncio.fixture
    async def script_sql(self):
        path = os.path.dirname(os.path.abspath(__file__))

        with open(f"{path}/../script.sql", "r") as file:
            script_sql = file.read()
            return script_sql

    @pytest_asyncio.fixture(autouse=True)
    async def setup(self, script_sql):
        os.environ["ENV"] = "TEST"
        os.environ["db_host"] = "localhost"
        os.environ["db_port"] = "5400"
        os.environ["db_name"] = "rinha"
        os.environ["db_user"] = "admin"
        os.environ["db_pass"] = "123"
        os.environ["pool_max_size"] = "2"

        self.pool = await create_pool()

        self.repositorio = TransacaoRepositorio(self.pool)

        async with self.pool.connection() as conn:
            await conn.execute(script_sql)

        async with self.pool.connection() as conn:
            await conn.execute("LOCK TABLE transacoes IN EXCLUSIVE MODE;")
            await conn.execute("DELETE FROM transacoes")
            await conn.execute("DELETE FROM clientes")

        yield

        async with self.pool.connection() as conn:
            await conn.execute("LOCK TABLE transacoes IN EXCLUSIVE MODE;")
            await conn.execute("DELETE FROM transacoes")
            await conn.execute("DELETE FROM clientes")

    @pytest_asyncio.fixture
    async def client_id(self):
        async with self.pool.connection() as conn:
            response = await conn.execute(
                "INSERT INTO clientes (nome, limite, saldo) VALUES ('rei do baiao',100000, 0) RETURNING id"
            )

            cliente_id = await response.fetchone()
            cliente_id = cliente_id[0]
            await conn.commit()
            yield cliente_id
            await conn.execute(
                f"DELETE FROM transacoes WHERE cliente_id = {cliente_id}"
            )
            await conn.execute(f"DELETE FROM clientes WHERE id = {cliente_id}")

    @pytest_asyncio.fixture()
    async def pool(self):
        return self.pool
