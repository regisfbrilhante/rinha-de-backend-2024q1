from psycopg import connect

from src.config import config


def create_connection():
    uri = f"postgresql://{config.get('db_user')}:{config.get('db_pass')}@{config.get('db_host')}:{config.get('db_port')}/{config.get('db_name')}"
    connection = connect(uri)
    return connection
