import os
import logging
import threading
import asyncio
from datetime import datetime
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncEngine
import colorlog

from server.core.functions.SqlDBFunctions import log_system


LOG_DIR = "./logs"
LOG_FORMAT_CONSOLE = "%(log_color)s%(levelname)-8s:%(reset)s %(message)s"
LOG_FORMAT_FILE = "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"


class SystemLogHandler(logging.Handler):
    def __init__(self, engine: AsyncEngine):
        super().__init__(level=logging.INFO)
        self.engine = engine
        self._pending = set()
        self._lock = threading.Lock()
        self._error_logger = logging.getLogger("system_log_errors")
        self._error_logger.setLevel(logging.ERROR)
        if not self._error_logger.hasHandlers():
            stderr_handler = logging.StreamHandler()
            stderr_handler.setFormatter(logging.Formatter("[FALLBACK] %(asctime)s - %(message)s"))
            self._error_logger.addHandler(stderr_handler)

    async def _write_to_db(self, message: str):
        try:
            async with self.engine.begin() as conn:
                await conn.execute(insert(log_system).values(message=message))
        except Exception:
            self._error_logger.error("Ошибка записи лога в БД: %s", message, exc_info=True)

    def emit(self, record: logging.LogRecord):
        msg = self.format(record)
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            self._error_logger.error("Нет запущенного asyncio-цикла. Пропущено сообщение: %s", msg)
            return

        task = loop.create_task(self._write_to_db(msg))
        with self._lock:
            self._pending.add(task)
        task.add_done_callback(lambda fut: self._remove_task(fut))

    def _remove_task(self, fut: asyncio.Future):
        with self._lock:
            self._pending.discard(fut)

    async def close_async(self):
        with self._lock:
            tasks = list(self._pending)
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        super().close()

    def close(self):
        try:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                loop = None

            if loop and loop.is_running():
                loop.create_task(self.close_async())
            else:
                asyncio.run(self.close_async())
        finally:
            super().close()


def setup_logger(engine: AsyncEngine) -> logging.Logger:
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d_%H-%M-%S")
    os.makedirs(LOG_DIR, exist_ok=True)
    log_file = os.path.join(LOG_DIR, f"{date_str}.log")

    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.INFO)

    if not logger.hasHandlers():
        ch = colorlog.StreamHandler()
        ch.setFormatter(colorlog.ColoredFormatter(LOG_FORMAT_CONSOLE))

        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setFormatter(logging.Formatter(LOG_FORMAT_FILE))

        dbh = SystemLogHandler(engine=engine)
        dbh.setFormatter(logging.Formatter("%(message)s"))

        for handler in (ch, fh, dbh):
            logger.addHandler(handler)

    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(logging.INFO)
    uvicorn_logger.propagate = True

    return logger

if __name__ == "__main__":
    from sqlalchemy.ext.asyncio import create_async_engine
    from .Config import settings

    engine = create_async_engine(settings.MYSQL_URL, echo=True)
    logger = setup_logger(engine)

    logger.info("Logger initialized successfully.")
    logger.error("This is an error message for testing.")
    
    asyncio.run(logger.handlers[2].close_async())
