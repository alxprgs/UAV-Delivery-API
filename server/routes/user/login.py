from secrets import token_urlsafe

from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy import insert

from datetime import datetime, timedelta

from server import app, client, db, engine
from server.core.api.configuringsqldb import login_logs
from server.core.api.schemes import UserAuthorization
from server.core.config import settings
from server.core.functions.hash import verify_hash
from server.core.functions.mongodb import check_connection
from server.core.logging_module import logger

MAX_ATTEMPTS = 5
WINDOW_MINUTES = 15

@app.post("/v1/user/login", tags=["user", "post"], summary="User Login", description="Allows a user to log in with their credentials.")
async def authorization(data: UserAuthorization, request: Request) -> JSONResponse:
    if not await check_connection(client):
        return JSONResponse(
            content={"status": False, "message": "Error connecting to the database. Internal Server Error."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    now = datetime.now()
    window_start = now - timedelta(minutes=WINDOW_MINUTES)
    attempts_coll = db["login_attempts"]
    attempts = await attempts_coll.count_documents({
        "login": data.login,
        "timestamp": {"$gte": window_start}
    })
    if attempts >= MAX_ATTEMPTS:
        return JSONResponse(
            content={"status": False, "message": f"Превышено количество попыток входа. Попробуйте снова через {WINDOW_MINUTES} минут."},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )
    await attempts_coll.insert_one({
        "login": data.login,
        "timestamp": now,
        "ip": request.headers.get("x-forwarded-for", request.client.host)
    })

    user = await db["users"].find_one({"login": data.login})
    if user is None or not verify_hash(data.password, user["password"]):
        return JSONResponse(
            content={"status": False, "message": "Invalid username or password. Unauthorized."},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    if verify_hash(text=data.password, stored_hash=user["password"]):
        token = token_urlsafe(64)
        await db["users"].find_one_and_update({"login": data.login}, {"$set": {"token": token}})
        response = JSONResponse(
            content={"status": True, "message": "Successful аuthorization. Ok."},
            status_code=status.HTTP_200_OK)
        response.set_cookie(key="token", value=token, domain=f".{settings.DOMAIN}", secure=True, httponly=True, samesite="Strict", max_age=3*24*60*60)
        try:
            async with engine.begin() as conn:
                await conn.execute(insert(login_logs), {
                    "login": data.login,
                    "ip_address": request.headers.get("x-forwarded-for", request.client.host),
                    "user_agent": request.headers.get("user-agent", "unknown")
                })
        except Exception as e:
            logger.warning("Failed to write login_log for %s: %s", data.login, e)
        return response