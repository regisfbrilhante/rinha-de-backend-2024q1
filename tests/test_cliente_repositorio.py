from datetime import datetime
from http import client

import pytest
import pytest_asyncio

from src.exceptions.exceptions import ClientNotFoundException
from src.repositorios.cliente_repositorio import ClienteRepositorio
from tests.test_base import TestBase


class TestClienteRepositorio(TestBase):

    @pytest_asyncio.fixture
    async def repositorio(self):
        return ClienteRepositorio(pool=self.pool)

    @pytest.mark.asyncio
    async def test_deve_retornar_o_extrato_do_cliente(
        self, repositorio: ClienteRepositorio, pool, client_id
    ):
        async with pool.connection() as conn:
            await conn.execute(
                "UPDATE clientes SET saldo = 49 WHERE id = %s", (client_id,)
            )

            await conn.execute(
                "INSERT INTO TRANSACOES (cliente_id, valor, tipo, descricao, saldo, data_transacao) VALUES (%s, 100, 'c', 'descricao', 100, '2024-01-01')",
                (client_id,),
            )

            await conn.execute(
                "INSERT INTO TRANSACOES (cliente_id, valor, tipo, descricao, saldo, data_transacao) VALUES (%s, 51, 'd', 'descricao', 49, '2024-01-02')",
                (client_id,),
            )

        extrato = await repositorio.get_extrato(cliente_id=client_id)

        assert extrato.saldo.total == 49
        assert extrato.saldo.limite == 100000
        assert extrato.saldo.data_extrato is not None
        assert len(extrato.ultimas_transacoes) == 2

    @pytest.mark.asyncio
    async def test_o_numero_maximo_das_ultimas_transacoes_no_extrato_deve_ser_10(
        self, repositorio: ClienteRepositorio, pool, client_id
    ):
        async with pool.connection() as conn:
            for i in range(12):
                await conn.execute(
                    "INSERT INTO TRANSACOES (cliente_id, valor, tipo, descricao, saldo, data_transacao) VALUES (%s, 51, 'd', 'descricao', 49, %s)",
                    (
                        client_id,
                        f"2024-01-0{i+1}",
                    ),
                )

        extrato = await repositorio.get_extrato(cliente_id=client_id)

        assert len(extrato.ultimas_transacoes) == 10

    @pytest.mark.asyncio
    async def test_deve_retornar_um_extrato_vazio_quando_nao_houver_transacoes(
        self, repositorio: ClienteRepositorio, pool, client_id
    ):
        extrato = await repositorio.get_extrato(cliente_id=client_id)

        assert extrato.saldo.total == 0
        assert extrato.saldo.limite == 100000
        assert extrato.saldo.data_extrato is not None
        assert len(extrato.ultimas_transacoes) == 0

    @pytest.mark.asyncio
    async def test_a_data_da_primeira_transacao_deve_ser_a_data_mais_recente_no_extrato(
        self, repositorio: ClienteRepositorio, pool, client_id
    ):
        async with pool.connection() as conn:
            await conn.execute(
                "INSERT INTO TRANSACOES (cliente_id, valor, tipo, descricao, saldo, data_transacao) VALUES (%s, 100, 'c', 'descricao', 100, '2024-01-01')",
                (client_id,),
            )
            await conn.execute(
                "INSERT INTO TRANSACOES (cliente_id, valor, tipo, descricao, saldo, data_transacao) VALUES (%s, 51, 'd', 'descricao', 49, '2024-01-02')",
                (client_id,),
            )

        extrato = await repositorio.get_extrato(cliente_id=client_id)

        assert extrato.ultimas_transacoes[0].realizada_em == datetime(
            year=2024, month=1, day=2
        )

    @pytest.mark.asyncio
    async def test_deve_retornar_um_erro_quando_o_cliente_nao_existir(
        self, repositorio: ClienteRepositorio
    ):
        with pytest.raises(ClientNotFoundException):
            await repositorio.get_extrato(cliente_id=-1)
