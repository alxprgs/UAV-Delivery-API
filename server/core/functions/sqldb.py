from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.exc import SQLAlchemyError

from server.core.logging_module import setup_logger
from server.core.api.configuringsqldb import system_logs, logs
from server.core.database.mysql import connect_mysql
from server import engine


logger = setup_logger(engine=engine)
async def _get_engine(engine: AsyncEngine = None) -> tuple[AsyncEngine, bool]:
    if engine is not None:
        return engine, False
    try:
        engine = await connect_mysql(show_log=False)
        return engine, True
    except Exception as e:
        logger.error("Failed to create engine: %s", e, exc_info=True)
        raise


async def _log_to_table(table, values: dict, engine: AsyncEngine = None):
    engine, should_dispose = await _get_engine(engine)
    try:
        async with engine.begin() as conn:
            await conn.execute(insert(table).values(**values))
    except SQLAlchemyError as e:
        logger.error("Database error while writing log: %s", e, exc_info=True)
    except Exception as e:
        logger.error("Unexpected error while writing log: %s", e, exc_info=True)
    finally:
        if should_dispose:
            await engine.dispose()


async def log_system(message: str, engine: AsyncEngine = None):
    await _log_to_table(system_logs, {"message": message}, engine)


async def log(action: str, details: str, user: str = "unknown", engine: AsyncEngine = None):
    await _log_to_table(logs, {"action": action, "details": details, "user": user}, engine)
