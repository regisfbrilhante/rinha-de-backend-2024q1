from psycopg_pool import AsyncConnectionPool, ConnectionPool

from src.config import config


def create_uri():
    uri = f"postgresql://{config.get('db_user')}:{config.get('db_pass')}@{config.get('db_host')}:{config.get('db_port')}/{config.get('db_name')}"
    return uri


async def create_pool():
    uri = create_uri()
    pool = AsyncConnectionPool(uri, max_size=10, min_size=10)

    # pool = await AsyncConnectionPool(uri, max_size=10, min_size=10)

    # pool_max_size = int(config.get("pool_max_size"))

    # pool = ConnectionPool(
    #     uri, min_size=pool_max_size, max_size=pool_max_size, open=True, timeout=5
    # )
    # pool.wait()
    return pool
