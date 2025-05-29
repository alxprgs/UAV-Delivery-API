from server import app, db
from fastapi import Request
from fastapi.responses import JSONResponse
from server.core.api.schemes import UserSetPasswordByAdmin
from server.core.functions.hash import create_hash
from server.core.functions.mongodb import check_permissions, get_user_login
from server.core.functions.sqldb import log_system
from server.core.logging import logger

@app.post("/v1/user/set_password", tags=["user", "post"], summary="Set user password by admin", description="Allows an admin to set a password for a user.")
async def set_user_password_by_admin(request: Request, data: UserSetPasswordByAdmin) -> JSONResponse:
    permission = await check_permissions(request=request, permission="set_user_password", database=db)
    if not permission:
        return JSONResponse(
            status_code=403,
            content={"status": False, "message": "You do not have permission to set user passwords."}
        )
    
    try:
        hashed_password = create_hash(data.password)
        result = await db["users"].update_one(
            {"login": data.login},
            {"$set": {"password": hashed_password}}
        )
        
        if result.modified_count == 0:
            return JSONResponse(
                status_code=404,
                content={"status": False, "message": "User not found or password already set."}
            )
        
        user_login = await get_user_login(request=request)
        await log_system(
            message=f"Password for user '{data.login}' set by {user_login}."
        )
        
        return JSONResponse(
            status_code=200,
            content={"status": True, "message": "Password successfully set."}
        )
    except Exception as e:
        logger.error("Error setting user password: %s", e, exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"status": False, "message": f"An error occurred while setting the password: {str(e)}"}
        )