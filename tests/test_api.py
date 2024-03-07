from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_get_extrato_deve_retornar_200_com_o_extrato_esperado():
    response = client.get("/clientes/1/extrato")
    assert response.status_code == 200
    assert response.json() == {
        "saldo": {
            "total": -9098,
            "data_extrato": "2024-01-17T02:34:41.217753Z",
            "limite": 100000,
        },
        "ultimas_transacoes": [
            {
                "valor": 10,
                "tipo": "c",
                "descricao": "descricao",
                "realizada_em": "2024-01-17T02:34:38.543030Z",
            },
            {
                "valor": 90000,
                "tipo": "d",
                "descricao": "descricao",
                "realizada_em": "2024-01-17T02:34:38.543030Z",
            },
        ],
    }


def test_post_deve_retornar_200_com_saldo_esperado():
    body = {"valor": 9000, "tipo": "c", "descricao": "descricao"}

    response = client.post("/clientes/1/transacoes", json=body)

    assert response.status_code == 200
    assert response.json() == {"limite": 100000, "saldo": -9098}
