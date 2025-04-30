from fastapi import FastAPI
from server.core.config import settings
from .core.tags_metadata import tags_metadata
from .core.database.mongodb import connect_mongo
from .core.database.mysql import connect_mysql
from .core.database.redis import connect_redis
from contextlib import asynccontextmanager
from typing import AsyncGenerator

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    global db, client, engine, redis_client
    db, client = await connect_mongo()
    engine = await connect_mysql()
    redis_client = await connect_redis()
    yield
    if client:
        client.close()
    if engine:
        await engine.dispose()
    if redis_client:
        await redis_client.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    license_info={
        "name": "Apache 2.0",
        "url": "https://github.com/alxprgs/UAV-Delivery-API?tab=Apache-2.0-1-ov-file#",
    },
    docs_url="/",
    redoc_url="/redoc"
) 