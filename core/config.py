from starlette.config import Config


config = Config(".env")

API_PREFIX: str = "/api"
VERSION: str = config("API_VERSION")
APP_NAME: str = config("APP_NAME")
DEBUG: bool = config("DEBUG", cast=bool, default=False)

POSTGRES_USER: str = config("POSTGRES_USER")
POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD")
POSTGRES_HOST: str = config("POSTGRES_HOST")
POSTGRES_PORT: str = config("POSTGRES_PORT", cast=int)
POSTGRES_DB: str = config("POSTGRES_DB")