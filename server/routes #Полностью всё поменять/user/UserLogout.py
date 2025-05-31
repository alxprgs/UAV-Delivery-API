from fastapi import status
from fastapi.responses import JSONResponse

from server import app
from server.core.config import settings

@app.get("/v1/user/logout", tags=["user", "get"], summary="User Logout", description="Logs out the user by clearing the authentication cookie.")
async def logout() -> JSONResponse:
    response = JSONResponse(content={"status": True, "message": "Successful account logout. Ок."}, status_code=status.HTTP_200_OK)
    response.delete_cookie(key="token", domain=f".{settings.DOMAIN}", secure=True, httponly=True, samesite="Strict")
    return response