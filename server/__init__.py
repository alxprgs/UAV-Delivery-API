from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from server.core.api.configuringmongodb import conf_mongodb
from server.core.api.configuringsqldb import metadata
from server.core.config import settings
from server.core.database.mongodb import connect_mongo
from server.core.database.mysql import connect_mysql
from server.core.database.redis import connect_redis
from server.core.RootUserCreate import root_user
from server.core.TagsMetadata import tags_metadata
from server.routes.user import UserAuthCheck, UserCheckPermissions, UserLogin, UserLogout, UserRegistration


class BlockMethodsMiddleware(BaseHTTPMiddleware):
    ALLOWED_METHODS = {"GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"}

    async def dispatch(self, request: Request, call_next):
        if request.method.upper() not in self.ALLOWED_METHODS:
            return JSONResponse(
                status_code=405,
                content={"status": False, "message": "Method not allowed"}
            )
        return await call_next(request)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    global db, client, engine, redis_client
    await conf_mongodb()
    db, client = await connect_mongo(show_log=True)
    engine = await connect_mysql(show_log=True)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)
    redis_client = await connect_redis(show_log=True)
    await root_user()
    from server.routes.user import UserPermissionSet
    from server.routes.files import robots, sitemap, ddos_tester
    from server.routes.orders import OrderCreate
    from server.routes.uav import UavAdd
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
    redoc_url="/redoc",
    debug=settings.DEV
)

app.add_middleware(BlockMethodsMiddleware)