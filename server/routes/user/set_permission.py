from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import insert

from server import app, db, engine
from server.core.api.configuringsqldb import permission_logs
from server.core.api.schemes import UserSetPermission
from server.core.functions.mongodb import check_permissions, get_user
from server.core.logging import logger

@app.patch("/v1/user/set_permissions", tags=["user", "patch"])
async def set_permissions(request: Request, data: UserSetPermission) -> JSONResponse:
    if await check_permissions(request=request, database=db, permission="set_permissions"):
        try:
            result = await db["users"].find_one_and_update(
                {"login": data.login},
                {"$set": {f"permissions.{data.permission}": data.value}}
            )
            if not result:
                return JSONResponse(
                content={"status": False, "message": "The user was not found. Not found."},
                status_code=status.HTTP_404_NOT_FOUND
                )

            current_user = await get_user(request, db)
            actor_login = current_user["login"] if current_user else "unknown"

            async with engine.begin() as conn:
                await conn.execute(
                    insert(permission_logs),{"message": f"User '{actor_login}' set permission '{data.permission}' to '{data.value}' for user '{data.login}'"})

            return JSONResponse(
                content={"status": True, "message": "Successful change of permission. Ok."},
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error("Exception while setting permission: %s", e, exc_info=True)
            return JSONResponse(
                content={"status": False, "message": "Error changing the permissions. Internal Server Error."},
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    return JSONResponse(
        content={"status": False, "message": "Not enough rights. Forbidden."},
        status_code=status.HTTP_403_FORBIDDEN
    )
