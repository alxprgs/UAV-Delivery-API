from server.core.logging import logger
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
from server.core.config import settings

async def connect_mysql():
    engine = create_async_engine(settings.MYSQL_URL)

    try:
        async with engine.connect() as mysql_db:
            await mysql_db.execute(text("SELECT 1"))
            logger.info("Успешное подключение к MySQL.")
            return engine
    except Exception as e:
        logger.critical("Ошибка подключения к MySQL: %s", str(e), exc_info=True)
        await engine.dispose()
        return None
