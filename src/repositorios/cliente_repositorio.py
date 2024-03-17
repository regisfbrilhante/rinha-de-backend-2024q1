from datetime import datetime

from src.exceptions.exceptions import ClientNotFoundException
from src.schemas.schemas import Extrato, Saldo, TransacaoRealizada


class ClienteRepositorio:
    def __init__(self, pool) -> None:
        self._pool = pool

    async def get_extrato(self, cliente_id: int):

        async with self._pool.connection() as conn:

            result = await conn.execute(
                "SELECT limite, saldo FROM clientes WHERE id = %s;", (cliente_id,)
            )

            result = await result.fetchone()

            if not result:
                raise ClientNotFoundException("Cliente não encontrado")

            (limite, saldo) = result

            ultimas_transacoes = []
            transacoes = await conn.execute(
                """SELECT valor, tipo , descricao, data_transacao, saldo
                FROM transacoes
                WHERE cliente_id = %s ORDER BY data_transacao DESC LIMIT 10;""",
                (cliente_id,),
            )
            transacoes = await transacoes.fetchall()

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

        return Extrato(
            ultimas_transacoes=ultimas_transacoes,
            saldo=Saldo(total=saldo, data_extrato=data_extrato, limite=limite),
        )
