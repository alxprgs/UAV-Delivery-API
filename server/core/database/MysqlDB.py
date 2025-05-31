from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from server import engine
from server.core.api.ConfiguringSqlDB import metadata
from server.core.Config import settings
from server.core.LoggingModule import setup_logger

logger = setup_logger(engine=engine)
async def connect_mysql(show_log: bool = True):
    engine = create_async_engine(settings.MYSQL_URL)

    try:
        async with engine.connect() as mysql_db:
            await mysql_db.execute(text("SELECT 1"))
            if show_log:
                logger.info("Успешное подключение к MySQL.")
            return engine
    except Exception as e:
        if show_log:
            logger.critical("Ошибка подключения к MySQL: %s", str(e), exc_info=True)
        await engine.dispose()
        return None
