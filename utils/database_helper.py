import psycopg_pool
from core import config

#conn_string = f'postgresql://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}?application_name={config.APP_NAME}'
conn_string = f'host={config.POSTGRES_HOST} user={config.POSTGRES_USER} password={config.POSTGRES_PASSWORD} dbname={config.POSTGRES_DB} port={config.POSTGRES_PORT}'

class DBConnectionPool:
    def __init__(self):
        self.psyco_async_pool: psycopg_pool.AsyncConnectionPool = psycopg_pool.AsyncConnectionPool(
            conn_string,
            min_size=4,
            max_size=10,
            open=False
        )
        
    async def close(self):
        await self.psyco_async_pool.close()
