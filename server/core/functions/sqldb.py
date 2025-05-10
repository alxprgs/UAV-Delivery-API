from sqlalchemy import insert

from server.core.api.configuringsqldb import system_logs
from server.core.database.mysql import connect_mysql


async def log_system(message: str):
    engine = await connect_mysql(show_log=False)
    try:
        async with engine.begin() as conn:
            await conn.execute(insert(system_logs).values(message=message))
            await engine.dispose()
    except Exception:
        pass