import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient

from tests.test_base import TestBase


class TesteApi(TestBase):

    @pytest_asyncio.fixture
    async def app(self):
        from src.main import app

        async with LifespanManager(app) as manager:
            yield manager.app

    @pytest_asyncio.fixture
    async def client(self, app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client

    @pytest.mark.asyncio
    async def test_root(self, client_id, client):
        from src.main import app

        async with AsyncClient(app=app, base_url="http://test") as client:
            body = {"valor": 10, "tipo": "d", "descricao": "descricao"}
            response = await client.post(f"/clientes/{client_id}/transacoes", json=body)

            assert response.status_code == 200
            assert response.json() == {"limite": 100000, "saldo": -10}

    @pytest.mark.asyncio
    @pytest.mark.parametrize("valor,saldo", [(1, 1), (10, 10), (1001, 1001)])
    async def test_quando_uma_operacao_de_credito_for_chamada_deve_adicionar_o_valor_ao_saldo_e_retornar_200(
        self, valor, saldo, client_id, client
    ):
        body = {"valor": valor, "tipo": "c", "descricao": "descricao"}
        response = await client.post(f"/clientes/{client_id}/transacoes", json=body)

        assert response.status_code == 200
        assert response.json() == {"limite": 100000, "saldo": saldo}

    @pytest.mark.asyncio
    async def test_quando_uma_operacao_de_debito_for_chamada_deve_subtrair_o_valor_do_saldo_e_retornar_200(
        self, client_id, client
    ):

        body = {"valor": 10, "tipo": "d", "descricao": "descricao"}
        response = await client.post(f"/clientes/{client_id}/transacoes", json=body)

        assert response.status_code == 200
        assert response.json() == {"limite": 100000, "saldo": -10}

    @pytest.mark.asyncio
    async def test_quando_o_limite_foi_atingido_deve_retornar_422(
        self, client_id, client
    ):
        body = {"valor": 100001, "tipo": "d", "descricao": "descricao"}
        response = await client.post(f"/clientes/{client_id}/transacoes", json=body)

        assert response.status_code == 422

    @pytest.mark.asyncio
    @pytest.mark.parametrize("operacao", ["c", "d"])
    async def test_quando_o_cliente_nao_existir_para_credito_ou_debito_deve_retornar_404(
        self, operacao, client
    ):
        body = {"valor": 100001, "tipo": operacao, "descricao": "descricao"}
        response = await client.post(f"/clientes/{-1}/transacoes", json=body)

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_quando_o_cliente_nao_existir_para_extrato_deve_retornar_404(
        self, client
    ):
        response = await client.get(f"/clientes/{-1}/extrato")

        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_get_extrato_deve_retornar_200_com_o_extrato_esperado(
        self, client_id, client
    ):
        response = await client.get(f"/clientes/{client_id}/extrato")

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["saldo"]["total"] == 0
        assert response_data["saldo"]["limite"] == 100000
        assert response_data["ultimas_transacoes"] == []

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "tipo,descricao,valor,id",
        [
            ("a", "descricao maior", 100.1, "a"),
            ("c", "descricao", 100, "a"),
            ("c", "descricao", 100, 1.1),
            ("c", "descricao", 100.1, 1),
            ("d", "descricao", 100.1, 1),
            ("c", "descricao maior", 100, 1),
            ("d", "descricao maior", 100, 1),
            ("c", "descricao", 100.1, 1),
            ("d", "descricao", 100.1, 1),
            ("a", "descricao", 100, 1),
            ("c", "descricao", -100, 1),
            ("c", "", 100, 1),
        ],
    )
    async def test_quando_o_payload_estiver_invalido_deve_retornar_422(
        self, tipo, descricao, valor, id, client
    ):
        body = {"valor": valor, "tipo": tipo, "descricao": descricao}
        response = await client.post(f"/clientes/{id}/transacoes", json=body)

        assert response.status_code == 422
