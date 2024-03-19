from psycopg_pool import AsyncConnectionPool, ConnectionPool

from src.config import config


def create_uri():
    uri = f"postgresql://{config.get('db_user')}:{config.get('db_pass')}@{config.get('db_host')}:{config.get('db_port')}/{config.get('db_name')}"
    return uri


async def create_pool():
    uri = create_uri()
    pool = AsyncConnectionPool(uri, max_size=5, min_size=5)
    return pool
