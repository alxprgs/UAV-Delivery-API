from server.core.functions.mongodb import check_auth
from server import app, db
from fastapi import Request

@app.get("/v1/user/check_auth", tags=["user", "get"])
async def auth_check(request: Request) -> bool:
    return await check_auth(request=request, database=db)