from datetime import datetime

from src.exceptions.exceptions import (BalanceLimitExceededException,
                                       ClientNotFoundException)
from src.schemas.schemas import ResultadoTransacao, Transacao


class TransacaoRepositorio:
    def __init__(self, pool) -> None:
        self._pool = pool

    def debito(self, cliente_id: int, transacao: Transacao) -> None:
        with self._pool.connection() as conn:
            result = conn.execute(
                "SELECT limite, saldo FROM clientes WHERE id = %s FOR UPDATE;",
                (cliente_id,),
            ).fetchone()

            if not result:
                raise ClientNotFoundException("Cliente não encontrado")

            limite, saldo_atual = result
            novo_saldo = saldo_atual - transacao.valor

            if novo_saldo < 0 and novo_saldo * -1 > limite:
                raise BalanceLimitExceededException("Saldo insuficiente")

            updated_date = datetime.utcnow()

            conn.execute(
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
            conn.execute(
                "UPDATE clientes SET saldo = %s WHERE id = %s;",
                (novo_saldo, cliente_id),
            )

            return ResultadoTransacao(limite=limite, saldo=novo_saldo)

    def credito(self, cliente_id: int, transacao: Transacao) -> ResultadoTransacao:

        with self._pool.connection() as conn:

            result = conn.execute(
                "SELECT limite, saldo FROM clientes WHERE id = %s FOR UPDATE;",
                (cliente_id,),
            ).fetchone()
            if not result:
                raise ClientNotFoundException("Cliente não encontrado")

            limite, saldo_atual = result

            novo_saldo = saldo_atual + transacao.valor

            updated_date = datetime.utcnow()

            conn.execute(
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

            conn.execute(
                "UPDATE clientes SET saldo = %s WHERE id = %s;",
                (novo_saldo, cliente_id),
            )

            return ResultadoTransacao(limite=limite, saldo=novo_saldo)
