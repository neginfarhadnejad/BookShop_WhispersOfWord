from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class CoreSettings(BaseSettings):
    SECRET_KEY: str = "nTn2J5NggXk4Vb6dwq6_jpAKrs6ZuCJ9oTUgFLlaF14"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 ساعت

    # سایر متغیرها
    DATABASE_DIALECT: str = "postgresql"
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")
    POSTGRES_HOST: str = Field(..., env="POSTGRES_HOST")
    POSTGRES_PORT: int = Field(..., env="POSTGRES_PORT")
    
    REDIS_URL: str = Field(..., env="REDIS_URL")
    REDIS_PORT: int = Field(..., env="REDIS_PORT")
    IAM_SERVICE_URL: str = Field(..., env="IAM_SERVICE_URL")
    
    DATABASE_USERNAME: str = Field(..., env="DATABASE_USERNAME")
    DATABASE_PASSWORD: str = Field(..., env="DATABASE_PASSWORD")
    
    DEBUG_MODE: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore"  # اضافه کردن extra="ignore" برای نادیده گرفتن پارامترهای اضافی
    )

def get_settings():
    return CoreSettings()  # بازگرداندن تنظیمات 
