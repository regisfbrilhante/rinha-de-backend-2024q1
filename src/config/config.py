import os


class Config:
    def __init__(self):
        self._config = {
            "db_host": "db",
            "db_port": 5432,
            "db_name": "rinha",
            "db_user": "admin",
            "db_pass": "123",
            "pool_max_size": 10,
        }

    def get(self, key: str) -> str:
        return os.environ.get(key, self._config[key])

    def get_config(self):
        return self._config
