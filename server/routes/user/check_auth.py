from fastapi import Request

from server import app, db
from server.core.functions.mongodb import check_auth

@app.get("/v1/user/check_auth", tags=["user", "get"], summary="Check user authentication", description="Checks if the user is authenticated and has the required permissions.")
async def auth_check(request: Request) -> bool:
    return await check_auth(request=request, database=db)