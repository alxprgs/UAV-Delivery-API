from server import app, db
from fastapi import Request
from fastapi.responses import JSONResponse
from server.core.api.schemes import DeleteBaseScheme
from server.core.functions.mongodb import check_permissions, get_user_login
from server.core.logging import logger
from server.core.functions.sqldb import log_system

@app.post("/v1/base/delete_base", tags=["base", "post"], summary="Delete base", description="Deletes a base from the database if user has the required permissions.")
async def delete_base(request: Request, data: DeleteBaseScheme) -> JSONResponse:
    permission = await check_permissions(request=request, permission="delete_base", database=db)
    if not permission:
        return JSONResponse(
            status_code=403,
            content={"status": False, "message": "You do not have permission to delete bases."}
        )
    
    try:
        result = await db["base"].delete_one({"name": data.name})
        if result.deleted_count == 0:
            return JSONResponse(
                status_code=404,
                content={"status": False, "message": "Base not found."}
            )
        
        user_login = await get_user_login(request=request)
        await log_system(
            message=f"Base '{data.name}' deleted {user_login}."
        )
        
        return JSONResponse(
            status_code=200,
            content={"status": True, "message": "Base successfully deleted."}
        )
    except Exception as e:
        logger.error("Error deleting base: %s", e, exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"status": False, "message": f"An error occurred while deleting the base: {str(e)}"}
        )