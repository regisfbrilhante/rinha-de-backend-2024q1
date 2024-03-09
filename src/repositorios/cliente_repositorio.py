from datetime import datetime

from schemas.schemas import Extrato, Saldo, TransacaoRealizada


class ClienteRepositorio:
    def __init__(self, connection) -> None:
        self._connection = connection

    def get_extrato(self, cliente_id: int):

        with self._connection.cursor() as cursor:
            # cursor.execute("SET TRANSACTION MODE READ COMMITTED")

            cursor.execute("SELECT limite FROM clientes WHERE id = %s;", (cliente_id,))
            limite = cursor.fetchone()

            if not limite:
                raise ValueError("Cliente não encontrado")

            limite = limite[0]

            ultimas_transacoes = []
            cursor.execute(
                """SELECT valor, tipo , descricao, data_transacao, saldo
                FROM transacoes
                WHERE cliente_id = %s
                ORDER BY data_transacao DESC LIMIT 10;""",
            )

        transacoes = cursor.fetchall()
        if not transacoes:
            ultimas_transacoes

        for transacao in transacoes:
            ultimas_transacoes.append(
                TransacaoRealizada(
                    valor=transacao[0],
                    tipo=transacao[1],
                    descricao=transacao[2],
                    realizada_em=transacao[3],
                )
            )

        data_extrato = datetime.utcnow()

        saldo_atual = transacoes[0]["saldo"]

        return Extrato(
            ultimas_transacoes=ultimas_transacoes,
            saldo=Saldo(total=saldo_atual, data_extrato=data_extrato, limite=limite),
        )
