import os

import pytest

from src.repositorios.pgsql_connection_factory import create_connection
from src.repositorios.transacao_repositorio import TransacaoRepositorio


class TestBase:

    # def __init__(self) -> None:

    #     os.environ["ENV"] = "TEST"
    #     os.environ["db_host"] = "localhost"
    #     os.environ["db_port"] = "5400"
    #     os.environ["db_name"] = "rinha"
    #     os.environ["db_user"] = "admin"
    #     os.environ["db_pass"] = "123"

    #     self.connection = create_connection()
    #     with self.connection.cursor() as cursor:
    #         # cursor.execute("LOCK TABLE transacoes IN EXCLUSIVE MODE;")
    #         # cursor.execute("LOCK TABLE clientes IN EXCLUSIVE MODE;")

    #         # cursor.execute("DROP TABLE IF EXISTS transacoes")
    #         # cursor.execute("DROP TABLE IF EXISTS clientes")

    #         cursor.execute(query=self.script_sql())

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

        self.connection = create_connection()
        self.repositorio = TransacaoRepositorio(self.connection)

        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM transacoes")
            cursor.execute("DELETE FROM clientes")
            cursor.execute(query=script_sql)
            self.connection.commit()

        yield

        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM transacoes")
            cursor.execute("DELETE FROM clientes")
            self.connection.commit()

        self.connection.close()

    @pytest.fixture()
    def client_id(self):
        with self.connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO clientes (nome, limite) VALUES ('rei do baiao',100000) RETURNING id"
            )
            cliente_id = cursor.fetchone()[0]
            self.connection.commit()
            yield cliente_id
            cursor.execute(f"DELETE FROM clientes WHERE id = {cliente_id}")

    @pytest.fixture()
    def connection(self):
        return self.connection
