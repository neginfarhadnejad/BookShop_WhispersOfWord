
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from datetime import timedelta

SECRET_KEY = "nTn2J5NggXk4Vb6dwq6_jpAKrs6ZuCJ9oTUgFLlaF14"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 

class Settings(BaseSettings):
    DATABASE_DIALECT: str = "postgresql"

    DATABASE_USERNAME: str = Field(..., env="POSTGRES_USER")
    DATABASE_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    DATABASE_HOSTNAME: str = Field(..., env="POSTGRES_HOST")
    DATABASE_PORT: str = Field(..., env="POSTGRES_PORT")
    DATABASE_NAME: str = Field(..., env="POSTGRES_DB")

    DEBUG_MODE: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )

def get_settings():
    return Settings()
