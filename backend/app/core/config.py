from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_DIALECT: str = "postgresql"
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_NAME: str
    DEBUG_MODE: bool = True

    class Config:
        env_file = ".env"


def get_settings():
    return Settings()
