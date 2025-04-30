from redis.asyncio import Redis
from server.core.logging import logger
from server.core.config import settings


async def connect_redis():
    redis_client = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5,
        retry_on_timeout=True
    )

    try:
        if await redis_client.ping():
            logger.info("Успешное подключение к Redis.")
            return redis_client
    except Exception as e:
        logger.critical("Ошибка подключения к redis: %s", e, exc_info=True)
        return None
