import os
import pytest
from src.repositorios.pgsql_connection_factory import create_connection

from src.repositorios.transacao_repositorio import TransacaoRepositorio


class TestBase:
    create_clientes_table = """
        CREATE TABLE CLIENTES (
        id SERIAL PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        limite INTEGER NOT NULL
        );
        """

    create_transacoes_table = """
        CREATE TABLE TRANSACOES (
        id SERIAL PRIMARY KEY,
        cliente_id INTEGER NOT NULL,
        valor INTEGER NOT NULL,
        descricao VARCHAR(10),
        saldo INTEGER NOT NULL,
        data_transacao TIMESTAMP NOT NULL,
        FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        );
        """

    @pytest.fixture(autouse=True)
    def setup(self):
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

            cursor.execute(query=self.create_clientes_table)
            cursor.execute(self.create_transacoes_table)
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
    def repositorio(self):
        return self.repositorio

    @pytest.fixture()
    def connection(self):
        return self.connection
