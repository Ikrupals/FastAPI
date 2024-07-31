import uvicorn
from fastapi import FastAPI

from contextlib import asynccontextmanager

from utils.database_helper import DBConnectionPool
from api.device import device
from core import config

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.async_pool = DBConnectionPool()
    await app.async_pool.psyco_async_pool.open()
    yield
    await app.async_pool.close()

def get_application() -> FastAPI:
    application = FastAPI(
        title=config.APP_NAME,
        debug=config.DEBUG,
        version=config.VERSION,
        lifespan=lifespan
    )

    application.include_router(device.router, prefix=config.API_PREFIX, tags=["Device"])
    return application

app = get_application()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)