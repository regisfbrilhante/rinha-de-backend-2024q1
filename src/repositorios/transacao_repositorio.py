from datetime import datetime

from src.main import Transacao


class TransacaoRepositorio:
    def __init__(self, connection) -> None:
        self._session = connection

    def debito(
        self,
        cliente_id: int,
        transacao: Transacao,
        limite: int,
    ) -> None:

        with self._session.cursor() as cursor:
            cursor.execute("LOCK TABLE transacoes IN SHARE ROW EXCLUSIVE MODE;")

            cursor.execute(
                "SELECT saldo FROM transacoes WHERE cliente_id = %s ORDER BY data_transacao DESC LIMIT 1;",
                (cliente_id,),
            )

            saldo_atual = cursor.fetchone()
            saldo_atual = saldo_atual[0] if saldo_atual else 0

            novo_saldo = saldo_atual - transacao.valor

            if novo_saldo < 0 and novo_saldo * -1 > limite:
                raise ValueError("Saldo insuficiente")

            updated_date = datetime.utcnow()

            cursor.execute(
                "INSERT INTO TRANSACOES (valor, descricao, cliente_id, saldo, data_transacao) VALUES (%s, %s, %s, %s, %s)",
                (
                    transacao.valor,
                    transacao.descricao,
                    cliente_id,
                    novo_saldo,
                    updated_date,
                ),
            )

        self._session.commit()
        return novo_saldo

    def credito(self, cliente_id: int, valor: int) -> None: ...
