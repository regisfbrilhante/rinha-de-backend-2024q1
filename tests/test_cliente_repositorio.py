from datetime import datetime
from http import client

import pytest

from src.repositorios.cliente_repositorio import ClienteRepositorio
from tests.test_base import TestBase


class TestClienteRepositorio(TestBase):

    @pytest.fixture
    def repositorio(self, connection):
        return ClienteRepositorio(connection)

    def test_deve_retornar_o_extrato_do_cliente(
        self, repositorio: ClienteRepositorio, connection, client_id
    ):
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO TRANSACOES (cliente_id, valor, tipo, descricao, saldo, data_transacao) VALUES (%s, 100, 'c', 'descricao', 100, '2024-01-01')",
                (client_id,),
            )
            cursor.execute(
                "INSERT INTO TRANSACOES (cliente_id, valor, tipo, descricao, saldo, data_transacao) VALUES (%s, 51, 'd', 'descricao', 49, '2024-01-02')",
                (client_id,),
            )

        connection.commit()

        extrato = repositorio.get_extrato(cliente_id=client_id)

        assert extrato.saldo.total == 49
        assert extrato.saldo.limite == 100000
        assert extrato.saldo.data_extrato is not None
        assert len(extrato.ultimas_transacoes) == 2

    def test_o_numero_maximo_das_ultimas_transacoes_no_extrato_deve_ser_10(
        self, repositorio: ClienteRepositorio, connection, client_id
    ):
        with connection.cursor() as cursor:
            for i in range(12):
                cursor.execute(
                    "INSERT INTO TRANSACOES (cliente_id, valor, tipo, descricao, saldo, data_transacao) VALUES (%s, 51, 'd', 'descricao', 49, %s)",
                    (
                        client_id,
                        f"2024-01-0{i+1}",
                    ),
                )

        connection.commit()

        extrato = repositorio.get_extrato(cliente_id=client_id)

        assert len(extrato.ultimas_transacoes) == 10

    def test_deve_retornar_um_extrato_vazio_quando_nao_houver_transacoes(
        self, repositorio: ClienteRepositorio, connection, client_id
    ):
        extrato = repositorio.get_extrato(cliente_id=client_id)

        assert extrato.saldo.total == 0
        assert extrato.saldo.limite == 100000
        assert extrato.saldo.data_extrato is not None
        assert len(extrato.ultimas_transacoes) == 0

    def test_a_data_da_primeira_transacao_deve_ser_a_data_mais_recente_no_extrato(
        self, repositorio: ClienteRepositorio, connection, client_id
    ):
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO TRANSACOES (cliente_id, valor, tipo, descricao, saldo, data_transacao) VALUES (%s, 100, 'c', 'descricao', 100, '2024-01-01')",
                (client_id,),
            )
            cursor.execute(
                "INSERT INTO TRANSACOES (cliente_id, valor, tipo, descricao, saldo, data_transacao) VALUES (%s, 51, 'd', 'descricao', 49, '2024-01-02')",
                (client_id,),
            )

        connection.commit()

        extrato = repositorio.get_extrato(cliente_id=client_id)

        assert extrato.ultimas_transacoes[0].realizada_em == datetime(
            year=2024, month=1, day=2
        )

    def test_deve_retornar_um_erro_quando_o_cliente_nao_existir(
        self, repositorio: ClienteRepositorio
    ):
        with pytest.raises(ValueError):
            repositorio.get_extrato(cliente_id=-1)
