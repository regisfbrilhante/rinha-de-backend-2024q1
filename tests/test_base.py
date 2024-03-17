import os

import pytest

from src.repositorios.pgsql_connection_factory import create_pool
from src.repositorios.transacao_repositorio import TransacaoRepositorio


class TestBase:

    @pytest.fixture()
    def script_sql(self):
        path = os.path.dirname(os.path.abspath(__file__))

        with open(f"{path}/../script.sql", "r") as file:
            script_sql = file.read()
            return script_sql

    @pytest.fixture(autouse=True)
    def setup(self, script_sql):
        os.environ["ENV"] = "TEST"
        os.environ["db_host"] = "localhost"
        os.environ["db_port"] = "5400"
        os.environ["db_name"] = "rinha"
        os.environ["db_user"] = "admin"
        os.environ["db_pass"] = "123"
        os.environ["pool_max_size"] = "2"

        self.pool = create_pool()

        self.repositorio = TransacaoRepositorio(self.pool)

        with self.pool.connection() as conn:
            conn.execute(script_sql)

        with self.pool.connection() as conn:
            conn.execute("LOCK TABLE transacoes IN EXCLUSIVE MODE;")
            conn.execute("DELETE FROM transacoes")
            conn.execute("DELETE FROM clientes")

        yield

        with self.pool.connection() as conn:
            conn.execute("LOCK TABLE transacoes IN EXCLUSIVE MODE;")
            conn.execute("DELETE FROM transacoes")
            conn.execute("DELETE FROM clientes")

    @pytest.fixture()
    def client_id(self):
        with self.pool.connection() as conn:
            cliente = conn.execute(
                "INSERT INTO clientes (nome, limite, saldo) VALUES ('rei do baiao',100000, 0) RETURNING id"
            )
            cliente_id = cliente.fetchone()[0]
            conn.commit()
            yield cliente_id
            conn.execute(f"DELETE FROM transacoes WHERE cliente_id = {cliente_id}")
            conn.execute(f"DELETE FROM clientes WHERE id = {cliente_id}")

    @pytest.fixture
    def pool(self):
        return self.pool
