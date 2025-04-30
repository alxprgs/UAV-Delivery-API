from typing import Optional
from pymongo.errors import ConnectionFailure
from server.core.config import settings

async def check_auth(request, database) -> Optional[dict]:
    token = request.cookies.get('token')
    if not token:
        return None
    return await database["users"].find_one({"token": token})

async def check_permissions(request, permission: str, database) -> bool:
    user = await check_auth(request, database)
    if not user:
        return False

    permissions = user.get("permissions")
    if not isinstance(permissions, dict):
        permissions = {}

    if permissions.get("dev", False) and settings.DEV:
        return True

    return permissions.get("all", False) or permissions.get(permission, False)

async def check_connection(mongo) -> bool:
    try:
        await mongo.admin.command('ping')
        return True
    except ConnectionFailure:
        return False
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")
        return False
