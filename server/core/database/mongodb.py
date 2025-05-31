from motor.motor_asyncio import AsyncIOMotorClient

from server import engine
from server.core.Config import settings
from server.core.LoggingModule import setup_logger

logger = setup_logger(engine=engine)
async def connect_mongo(show_log: bool = True):
    try:
        client = AsyncIOMotorClient(
            settings.MONGO_URL,
            serverSelectionTimeoutMS=5000,
            socketTimeoutMS=5000,
        )
        await client.admin.command("ping")
    except Exception as e:
        if show_log:
            logger.critical("Ошибка подключения к MongoDB: %s", e, exc_info=True)
        return None, None

    db = client[settings.MONGO_DB]
    if show_log:
        logger.info("Успешное подключение к MongoDB.")
    return db, client
