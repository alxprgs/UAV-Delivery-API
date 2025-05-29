from typing import Optional

from fastapi import Request
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure

from server.core.config import settings
from server.core.logging import logger

async def get_user(request: Request, database: AsyncIOMotorDatabase) -> Optional[dict]:
    token = request.cookies.get('token')
    if not token:
        return None
    try:
        return await database["users"].find_one({"token": token})
    except Exception as e:
        logger.error("Ошибка при получении пользователя: %s", e, exc_info=True)
        return None

async def check_auth(request: Request, database: AsyncIOMotorDatabase) -> bool:
    return await get_user(request, database) is not None

async def check_permissions(request: Request, permission: str, database: AsyncIOMotorDatabase) -> bool:
    user = await get_user(request, database)
    if not user:
        return False

    permissions = user.get("permissions") or {}
    if not isinstance(permissions, dict):
        return False

    if permissions.get("dev") and settings.DEV:
        return True

    return bool(permissions.get("all") or permissions.get(permission))

async def check_connection(mongo) -> bool:
    try:
        await mongo.admin.command('ping')
        return True
    except ConnectionFailure as cf:
        logger.error("Ошибка подключения к MongoDB: %s", cf, exc_info=True)
        return False
    except Exception as e:
        logger.error("Неожиданная ошибка при проверке соединения: %s", e, exc_info=True)
        return False

async def get_user_login(request: Request, database: AsyncIOMotorDatabase) -> Optional[str]:
    user = await get_user(request, database)
    if user:
        return user.get("login")
    return None