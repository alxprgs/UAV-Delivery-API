from server import app, db
from fastapi import Request
from fastapi.responses import JSONResponse
from server.core.api.schemes import AddBaseScheme
from server.core.functions.mongodb import check_permissions


@app.post("/v1/base/add_base", tags=["base", "post"], summary="Add new base", description="Adds a new base to the database if user has the required permissions.")
async def add_base(request: Request, data: AddBaseScheme) -> JSONResponse:
    prmission = await check_permissions(request=request, permission="add_base", database=db)
    if not prmission:
        return JSONResponse(
            status_code=403,
            content={"status": False, "message": "You do not have permission to add bases."}
        )
    try:
        existing = await db["base"].find_one({"name": data.name})
        if existing:
            return JSONResponse(
                status_code=409,
                content={"status": False, "message": "Base with this name already exists."}
            )

        await db["base"].insert_one({
            "name": data.name,
            "location": data.location,
            "description": data.description
        })
        return JSONResponse(
            status_code=201,
            content={"status": True, "message": "Base successfully added."}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": False, "message": f"An error occurred while adding the base: {str(e)}"}
        )