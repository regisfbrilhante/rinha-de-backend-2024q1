from datetime import datetime

from src.exceptions.exceptions import (BalanceLimitExceededException,
                                       ClientNotFoundException)
from src.schemas.schemas import ResultadoTransacao, Transacao


class TransacaoRepositorio:
    def __init__(self, pool) -> None:
        self._pool = pool

    async def debito(self, cliente_id: int, transacao: Transacao) -> None:
        async with self._pool.connection() as conn:
            result = await conn.execute(
                "SELECT limite, saldo FROM clientes WHERE id = %s FOR UPDATE;",
                (cliente_id,),
            )

            result = await result.fetchone()

            if not result:
                raise ClientNotFoundException("Cliente não encontrado")

            limite, saldo_atual = result
            novo_saldo = saldo_atual - transacao.valor

            if novo_saldo < 0 and novo_saldo * -1 > limite:
                raise BalanceLimitExceededException("Saldo insuficiente")

            updated_date = datetime.utcnow()

            await conn.execute(
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

            await conn.execute(
                "UPDATE clientes SET saldo = %s WHERE id = %s;",
                (novo_saldo, cliente_id),
            )

            return ResultadoTransacao(limite=limite, saldo=novo_saldo)

    async def credito(
        self, cliente_id: int, transacao: Transacao
    ) -> ResultadoTransacao:

        async with self._pool.connection() as conn:

            result = await conn.execute(
                "SELECT limite, saldo FROM clientes WHERE id = %s FOR UPDATE;",
                (cliente_id,),
            )

            result = await result.fetchone()

            if not result:
                raise ClientNotFoundException("Cliente não encontrado")

            limite, saldo_atual = result

            novo_saldo = saldo_atual + transacao.valor

            updated_date = datetime.utcnow()

            await conn.execute(
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

            await conn.execute(
                "UPDATE clientes SET saldo = %s WHERE id = %s;",
                (novo_saldo, cliente_id),
            )

            return ResultadoTransacao(limite=limite, saldo=novo_saldo)
