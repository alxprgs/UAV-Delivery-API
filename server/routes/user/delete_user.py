from server import app, db
from fastapi import Request
from fastapi.responses import JSONResponse
from server.core.api.schemes import UserDelete
from server.core.logging import logger
from server.core.functions.mongodb import check_permissions, get_user_login
from server.core.functions.sqldb import log_system

@app.post("/v1/user/delete_user", tags=["user", "post"], summary="Delete user", description="Deletes a user from the database if the user has the required permissions.")
async def delete_user(request: Request, data: UserDelete) -> JSONResponse:
    permission = await check_permissions(request=request, permission="delete_user", database=db)
    if not permission:
        return JSONResponse(
            status_code=403,
            content={"status": False, "message": "You do not have permission to delete users."}
        )
    
    try:
        result = await db["users"].delete_one({"login": data.login})
        if result.deleted_count == 0:
            return JSONResponse(
                status_code=404,
                content={"status": False, "message": "User not found."}
            )
        
        user_login = await get_user_login(request=request, database=db)
        await log_system(
            message=f"User '{data.login}' deleted by {user_login}."
        )
        
        return JSONResponse(
            status_code=200,
            content={"status": True, "message": "User successfully deleted."}
        )
    except Exception as e:
        logger.error("Error deleting user: %s", e, exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"status": False, "message": f"An error occurred while deleting the user: {str(e)}"}
        )