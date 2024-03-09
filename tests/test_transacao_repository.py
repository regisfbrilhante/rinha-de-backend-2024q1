import pytest
from src.schemas.schemas import Transacao

from src.repositorios.transacao_repositorio import TransacaoRepositorio

from tests.test_base import TestBase


class TestTransacaoRepository(TestBase):

    def test_quando_o_limite_foi_atingido_deve_lancar_uma_excecao(
        self, repositorio: TransacaoRepositorio, connection
    ):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE clientes SET limite = 1 WHERE id = 1")
        connection.commit()

        transacao = Transacao(descricao="descricao", tipo="d", valor=2)

        with pytest.raises(Exception):
            repositorio.debito(cliente_id=1, transacao=transacao, limite=1)

    def test_quando_o_limite_nao_foi_atingido_deve_realizar_o_debito(
        self, repositorio: TransacaoRepositorio, connection
    ):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE clientes SET limite = 1 WHERE id = 1")
        connection.commit()

        transacao = Transacao(descricao="descricao", tipo="d", valor=1)
        resultado = repositorio.debito(cliente_id=1, transacao=transacao, limite=1)

        with connection.cursor() as cursor:
            cursor.execute("SELECT saldo FROM transacoes WHERE cliente_id = 1")
            saldo = cursor.fetchone()
        assert saldo[0] == -1

        assert resultado.limite == 1
        assert resultado.saldo == -1

    def test_quando_a_operacao_for_de_credito_deve_creditar_o_valor(
        self, repositorio: TransacaoRepositorio, connection
    ):
        with connection.cursor() as cursor:
            cursor.execute("UPDATE clientes SET limite = 1 WHERE id = 1")
        connection.commit()

        transacao = Transacao(descricao="descricao", tipo="c", valor=1)
        resultado = repositorio.credito(cliente_id=1, transacao=transacao, limite=1)

        with connection.cursor() as cursor:
            cursor.execute("SELECT saldo FROM transacoes WHERE cliente_id = 1")
            saldo = cursor.fetchone()

        assert saldo[0] == 1
        assert resultado.limite == 1
        assert resultado.saldo == 1
