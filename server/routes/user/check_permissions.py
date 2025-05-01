from server import app, db
from fastapi import Request, Query
from server.core.functions.mongodb import check_permissions

@app.get("/v1/user/check_permissions", tags=["user", "get"])
async def permissions_check(request: Request, permission: str = Query(..., min_length=1, description="Name of the permission to check")) -> bool:
    return await check_permissions(request=request, permission=permission, database=db)
