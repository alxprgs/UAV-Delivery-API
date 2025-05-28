from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings(BaseSettings):
    MONGO_URL: str
    MYSQL_URL: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD : str
    MONGO_DB: str = "UAV-DELIVERY"
    ALGORITHM: str = "HS256"
    DEV: bool = False
    CORS_ORIGINS: list[str] = ["*"]
    SERVER_PORT: int = 5005
    PROJECT_NAME: str = "API for a website for delivery using UAVs"
    VERSION: str = "DEV 2.2.2 | Build 29.05.2025"
    ROOTUSER_PASSWORD: str = "root"
    DOMAIN: str = "api.asfes.ru"
    TEST_BASE_URL: str = "api.asfes.ru",
    YOOKASSA_SHOP_ID: int
    YOOKASSA_SECRET_KEY: str
    
    class Config:
        env_file = ".env"

settings = Settings()
