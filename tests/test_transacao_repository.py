import pytest

from src.exceptions.exceptions import BalanceLimitExceededException
from src.repositorios.transacao_repositorio import TransacaoRepositorio
from src.schemas.schemas import Transacao
from tests.test_base import TestBase


class TestTransacaoRepository(TestBase):

    @pytest.fixture
    def repositorio(self, connection):
        return TransacaoRepositorio(connection)

    def test_quando_o_limite_foi_atingido_deve_lancar_uma_excecao(
        self, repositorio: TransacaoRepositorio, client_id
    ):

        transacao = Transacao(descricao="descricao", tipo="d", valor=100001)

        with pytest.raises(BalanceLimitExceededException):
            repositorio.debito(cliente_id=client_id, transacao=transacao)

    def test_quando_o_limite_nao_foi_atingido_deve_realizar_o_debito(
        self, repositorio: TransacaoRepositorio, connection, client_id
    ):

        transacao = Transacao(descricao="descricao", tipo="d", valor=3)
        resultado = repositorio.debito(cliente_id=client_id, transacao=transacao)

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT saldo FROM transacoes WHERE cliente_id = %s", (client_id,)
            )
            saldo = cursor.fetchone()
        assert saldo[0] == -3

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT cliente_id, valor, tipo , descricao, saldo, data_transacao FROM transacoes WHERE cliente_id = %s",
                (client_id,),
            )
            transacoes = cursor.fetchall()
        assert len(transacoes) == 1
        assert transacoes[0][1] == 3
        assert transacoes[0][2] == "d"
        assert transacoes[0][3] == "descricao"
        assert transacoes[0][4] is not None

        assert resultado.limite == 100000
        assert resultado.saldo == -3

    def test_quando_a_operacao_for_de_credito_deve_creditar_o_valor(
        self, repositorio: TransacaoRepositorio, connection, client_id
    ):

        transacao = Transacao(descricao="descricao", tipo="c", valor=1)
        resultado = repositorio.credito(cliente_id=client_id, transacao=transacao)

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT saldo FROM transacoes WHERE cliente_id = %s", (client_id,)
            )
            saldo = cursor.fetchone()

        assert saldo[0] == 1
        assert resultado.limite == 100000
        assert resultado.saldo == 1
