from fastapi import Query, Request

from server import app, db
from server.core.functions.MongoDBFunctions import check_permissions

@app.get("/v1/user/check_permissions", tags=["user", "get"], summary="Check user permissions", description="Checks if the user has the specified permission.")
async def permissions_check(request: Request, permission: str = Query(..., min_length=1, description="Name of the permission to check")) -> bool:
    return await check_permissions(request=request, permission=permission, database=db)
