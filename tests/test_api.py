import os
from fastapi.testclient import TestClient
import pytest
from tests.test_base import TestBase


class TesteApi(TestBase):
    @pytest.fixture(autouse=True)
    def setup_api(self, setup):
        # TODO: melhorar injeção de dependência e realizar o import fora do método
        from src.main import app

        client = TestClient(app)
        self.client = client

    @pytest.mark.parametrize("valor,saldo", [(1, 1), (10, 10), (1001, 1001)])
    def test_quando_uma_operacao_de_credito_for_chamada_deve_adicionar_o_valor_ao_saldo_e_retornar_200(
        self, valor, saldo
    ):
        body = {"valor": valor, "tipo": "c", "descricao": "descricao"}
        response = self.client.post("/clientes/1/transacoes", json=body)
        response = self.client.post("/clientes/1/transacoes", json=body)

        assert response.status_code == 200
        assert response.json() == {"limite": 1000, "saldo": saldo}

    def test_get_extrato_deve_retornar_200_com_o_extrato_esperado(self):
        body = {"valor": 10, "tipo": "c", "descricao": "descricao"}
        response = self.client.get("/clientes/1/extrato")
        response = self.client.get("/clientes/1/extrato")

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["saldo"]["total"] == 10
        assert response_data["saldo"]["limite"] == 1000

        assert len(response_data["ultimas_transacoes"]) == 1
        assert response_data["ultimas_transacoes"][0]["valor"] == 10
        assert response_data["ultimas_transacoes"][0]["tipo"] == "c"
        assert response_data["ultimas_transacoes"][0]["descricao"] == "descricao"
        # assert response_data["ultimas_transacoes"][0]["realizada_em"] is not None


# def test_post_deve_retornar_200_com_saldo_esperado():
#     body = {"valor": 9000, "tipo": "c", "descricao": "descricao"}

#     response = client.post("/clientes/1/transacoes", json=body)

#     assert response.status_code == 200
#     assert response.json() == {"limite": 100000, "saldo": -9098}
