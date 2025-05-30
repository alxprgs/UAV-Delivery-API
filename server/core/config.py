from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv(override=True)

class Settings(BaseSettings):
    MONGO_URL: str = "mongodb://localhost:27017"
    MYSQL_URL: str = "mysql+sqlalchemy://root:password@localhost:3306/uav_delivery"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD : str
    MONGO_DB: str = "UAV-DELIVERY"
    ALGORITHM: str = "HS256"
    DEV: bool = False
    CORS_ORIGINS: list[str] = ["*"]
    SERVER_PORT: int = 5005
    PROJECT_NAME: str = "API for a website for delivery using UAVs"
    VERSION: str = "DEV 2.2.5 | Build 30.05.2025"
    ROOTUSER_PASSWORD: str = "root"
    DOMAIN: str = "api.asfes.ru"
    TEST_BASE_URL: str = "api.asfes.ru",
    YOOKASSA_SHOP_ID: int = None
    YOOKASSA_SECRET_KEY: str = None
    
    class Config:
        env_file = ".env"

settings = Settings()
