from secrets import token_urlsafe

from fastapi import Request, status
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError
from sqlalchemy import insert

from datetime import datetime, timedelta

from server import app, client, db, engine
from server.core.api.configuringsqldb import registration_logs
from server.core.api.schemes import UserRegistration
from server.core.config import settings
from server.core.functions.hash import create_hash
from server.core.functions.mongodb import check_connection
from server.core.logging_module import logger

MAX_REG_ATTEMPTS = 5
REG_WINDOW_MINUTES = 30


@app.post("/v1/user/registration", tags=["user", "post"], summary="User Registration", description="Allows a user to register with their credentials.")
async def registration(data: UserRegistration, request: Request) -> JSONResponse:
    if not await check_connection(client):
        return JSONResponse(
            content={"status": False, "message": "Error connecting to the database. Internal Server Error."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    now = datetime.now()
    window_start = now - timedelta(minutes=REG_WINDOW_MINUTES)
    reg_attempts_coll = db["registration_attempts"]
    ip = request.headers.get("x-forwarded-for", request.client.host)
    attempts = await reg_attempts_coll.count_documents({
        "ip": ip,
        "timestamp": {"$gte": window_start}
    })
    if attempts >= MAX_REG_ATTEMPTS:
        return JSONResponse(
            content={"status": False, "message": f"Превышено количество попыток регистрации. Попробуйте снова через {REG_WINDOW_MINUTES} минут."},
            status_code=status.HTTP_429_TOO_MANY_REQUESTS
        )
    await reg_attempts_coll.insert_one({
        "ip": ip,
        "timestamp": now
    })

    for field in ("login", "mail", "phone"):
        if await db["users"].find_one({field: getattr(data, field)}):
            return JSONResponse(
                content={"status": False, "message": f"{field.capitalize()} already exists. Conflict."},
                status_code=status.HTTP_409_CONFLICT)

    password = create_hash(text=data.password)
    token = token_urlsafe(64)

    try:
        await db["users"].insert_one({
            "login": data.login,
            "mail": data.mail,
            "phone": data.phone,
            "password": password,
            "token": token,
            "lastip": request.headers.get("x-forwarded-for", request.client.host)
        })
        response = JSONResponse(
            content={"status": True, "message": "Successful registration. Created."},
            status_code=status.HTTP_201_CREATED)
        response.set_cookie(key="token", value=token, domain=f".{settings.DOMAIN}", secure=True, httponly=True, samesite="Strict", max_age=3*24*60*60)
        try:
            async with engine.begin() as conn:
                await conn.execute(insert(registration_logs), {
                    "login": data.login,
                    "ip_address": request.headers.get("x-forwarded-for", request.client.host),
                    "user_agent": request.headers.get("user-agent", "unknown")
                })
        except Exception as e:
            logger.warning("Failed to write login_log for %s: %s", data.login, e)

        return response

    except DuplicateKeyError:
        return JSONResponse(
            content={"status": False, "message": "Account with provided credentials already exists."},
            status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        logger.error("Registration failed: %s", e, exc_info=True)
        return JSONResponse(
            content={"status": False, "message": "Internal Server Error."},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)