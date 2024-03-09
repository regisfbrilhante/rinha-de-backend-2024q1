class ClientNotFoundException(Exception):
    def __init__(self, name: str):
        self.name = name


class BalanceLimitExceededException(Exception):
    def __init__(self, name: str):
        self.name = name
