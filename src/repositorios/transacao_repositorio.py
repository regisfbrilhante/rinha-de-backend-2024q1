from datetime import datetime

from src.exceptions.exceptions import BalanceLimitExceededException
from src.schemas.schemas import ResultadoTransacao, Transacao


class TransacaoRepositorio:
    def __init__(self, connection) -> None:
        self._session = connection

    def get_limite(self, cliente_id: int) -> int:
        with self._session.cursor() as cursor:
            cursor.execute("SELECT limite FROM clientes WHERE id = %s;", (cliente_id,))
            limite = cursor.fetchone()

            if not limite:
                raise ValueError("Cliente não encontrado")

            limite = limite[0]

        return limite

    def debito(self, cliente_id: int, transacao: Transacao) -> None:
        limite = self.get_limite(cliente_id)

        with self._session.cursor() as cursor:
            cursor.execute("LOCK TABLE transacoes IN EXCLUSIVE MODE;")

            cursor.execute(
                "SELECT saldo FROM transacoes WHERE cliente_id = %s ORDER BY data_transacao DESC LIMIT 1;",
                (cliente_id,),
            )

            saldo_atual = cursor.fetchone()
            saldo_atual = saldo_atual[0] if saldo_atual else 0

            novo_saldo = saldo_atual - transacao.valor

            if novo_saldo < 0 and novo_saldo * -1 > limite:
                cursor.execute("ROLLBACK;")
                raise BalanceLimitExceededException("Saldo insuficiente")

            updated_date = datetime.utcnow()

            cursor.execute(
                "INSERT INTO TRANSACOES (valor, descricao, cliente_id, saldo, data_transacao, tipo) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    transacao.valor,
                    transacao.descricao,
                    cliente_id,
                    novo_saldo,
                    updated_date,
                    transacao.tipo,
                ),
            )

        self._session.commit()

        return ResultadoTransacao(limite=limite, saldo=novo_saldo)

    def credito(self, cliente_id: int, transacao: Transacao) -> ResultadoTransacao:
        limite = self.get_limite(cliente_id)
        with self._session.cursor() as cursor:

            cursor.execute("LOCK TABLE transacoes IN EXCLUSIVE MODE;")

            cursor.execute(
                "SELECT saldo FROM transacoes WHERE cliente_id = %s ORDER BY data_transacao DESC LIMIT 1;",
                (cliente_id,),
            )

            saldo_atual = cursor.fetchone()
            saldo_atual = saldo_atual[0] if saldo_atual else 0

            novo_saldo = saldo_atual + transacao.valor

            updated_date = datetime.utcnow()

            cursor.execute(
                "INSERT INTO TRANSACOES (valor, descricao, cliente_id, saldo, data_transacao, tipo) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    transacao.valor,
                    transacao.descricao,
                    cliente_id,
                    novo_saldo,
                    updated_date,
                    transacao.tipo,
                ),
            )

        self._session.commit()
        return ResultadoTransacao(limite=limite, saldo=novo_saldo)
