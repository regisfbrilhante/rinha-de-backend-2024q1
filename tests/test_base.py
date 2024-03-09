import os
import pytest
from src.repositorios.pgsql_connection_factory import create_connection

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

        self.connection = create_connection()
        self.repositorio = TransacaoRepositorio(self.connection)

        with self.connection.cursor() as cursor:
            cursor.execute("DROP TABLE IF EXISTS transacoes")
            cursor.execute("DROP TABLE IF EXISTS clientes")

            cursor.execute(query=script_sql)
            # cursor.execute(self.create_transacoes_table)
            self.connection.commit()
            cursor.execute(
                "INSERT INTO clientes (nome, limite) VALUES ('cliente', 1000)"
            )
            self.connection.commit()

        yield

        with self.connection.cursor() as cursor:
            cursor.execute("DROP TABLE transacoes")
            cursor.execute("DROP TABLE clientes")
            self.connection.commit()

        self.connection.close()

    @pytest.fixture()
    def connection(self):
        return self.connection
