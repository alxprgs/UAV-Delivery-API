from server import app, db
from server.core.LoggingModule import logger
from fastapi import Request
from server.core.api.schemes import DeleteUAVScheme
from fastapi.responses import JSONResponse
from server.core.functions.MongoDBFunctions import check_permissions, get_user_login
from server.core.functions.SqlDBFunctions import log_system

@app.post("/v1/uav/delete_uav", tags=["uav", "post"], summary="Delete UAV", description="Deletes a UAV from the database if user has the required permissions.")
async def delete_uav(request: Request, data: DeleteUAVScheme) -> JSONResponse:
    permission = await check_permissions(request=request, permission="delete_uav", database=db)
    if not permission:
        return JSONResponse(
            status_code=403,
            content={"status": False, "message": "You do not have permission to delete UAVs."}
        )
    
    try:
        result = await db["uav"].delete_one({"serial_number": data.serial_number})
        if result.deleted_count == 0:
            return JSONResponse(
                status_code=404,
                content={"status": False, "message": "UAV not found."}
            )
        
        user_login = await get_user_login(request=request, database=db)
        await log_system(
            message=f"UAV '{data.serial_number}' deleted by {user_login}."
        )
        
        return JSONResponse(
            status_code=200,
            content={"status": True, "message": "UAV successfully deleted."}
        )
    except Exception as e:
        logger.error("Error deleting UAV: %s", e, exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"status": False, "message": f"An error occurred while deleting the UAV: {str(e)}"}
        )