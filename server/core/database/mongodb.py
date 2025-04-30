from motor.motor_asyncio import AsyncIOMotorClient
from server.core.logging import logger
from server.core.config import settings

async def connect_mongo():
    try:
        client = AsyncIOMotorClient(
            settings.MONGO_URL,
            serverSelectionTimeoutMS=5000,
            socketTimeoutMS=5000,
        )
        await client.admin.command("ping")
    except Exception as e:
        logger.critical("Ошибка подключения к MongoDB: %s", e, exc_info=True)
        return None, None

    db = client[settings.MONGO_DB]
    logger.info("Успешное подключение к MongoDB.")
    return db, client
