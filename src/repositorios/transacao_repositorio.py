class TransacaoRepositorio:
    def __init__(self, session) -> None:
        self._session = session

    def adicionar_saldo(cliente_id: int, valor: int): ...

    def remover_saldo(cliente_id, valor: int): ...
