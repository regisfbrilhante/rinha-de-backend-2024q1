from datetime import datetime

from main import Transacao


class ValidadorTransacao:
    def validar(self, limite: int, saldo, valor: int) -> None: ...


class ValidarDebito:
    def validar(self, limite: int, saldo: int, valor: int) -> None:
        if (saldo + valor) > limite:
            raise ValueError("Saldo insuficiente")


class TransacaoRepositorio:
    def __init__(self, connection) -> None:
        self._session = connection

    def debito(
        self,
        cliente_id: int,
        transacao: Transacao,
        limite: int,
        validador: ValidadorTransacao,
    ) -> None:
        updated_date = datetime.utc.now()

        with self._session.cursor() as cursor:
            saldo_atual = cursor.execute(
                "SELECT saldo FROM client WHERE cliente_id = %s", (cliente_id,)
            )

            validador.validar(limite, saldo_atual, transacao.valor)

            cursor.execute(
                "INSERT INTO TRANSACAO (valor, descricao, cliente_id, data) VALUES (%s, %s, %s, %s, %s)",
                (transacao.valor, transacao.descricao, cliente_id, updated_date),
            )

            novo_saldo = saldo_atual - transacao.valor

            cursor.execute(
                """
                UPDATE saldo SET total = total + %s WHERE cliente_id = %s;
                """,
                (novo_saldo, cliente_id),
            )

            return limite, novo_saldo

    def credito(self, cliente_id: int, valor: int) -> None: ...