from server import app, db
from server.core.logging_module import logger
from fastapi import Request
from server.core.functions.mongodb import check_permissions
from server.core.api.schemes import AddUAVScheme
from fastapi.responses import JSONResponse
from pymongo.errors import DuplicateKeyError

@app.post("/v1/uav/add_uav", tags=["uav", "post"], summary="Add new UAV", description="Adds a new UAV to the database if user has the required permissions.")
async def add_uav(data: AddUAVScheme, request: Request) -> JSONResponse:
    adm = await check_permissions(request=request, permission="add_uav", database=db)
    if not adm:
        return JSONResponse(
            status_code=403,
            content={"status": False, "message": "You do not have permission to add UAVs."}
        )
    try:
        existing = await db["uav"].find_one({"serial_number": data.serial_number})
        if existing:
            return JSONResponse(
                status_code=409,
                content={"status": False, "message": "UAV with this serial number already exists."}
            )
        existing = await db["uav"].find_one({"name": data.name})
        if existing:
            return JSONResponse(
                status_code=409,
                content={"status": False, "message": "UAV with this name already exists."}
            )

        await db["uav"].insert_one({
            "name": data.name,
            "location": data.location,
            "coordinates": data.coordinates,
            "max_weigh_speedt": data.max_weight,
            "max": data.max_speed,
            "serial_number": data.serial_number,
            "battery": {
                "battery_capacity": data.battery_capacity,
                "battery_voltage": data.battery_voltage,
                "battery_charge": data.battery_charge,
                "battery_status": data.battery_status
            }
        })
        return JSONResponse(
            status_code=201,
            content={"status": True, "message": "UAV successfully added."}
        )
    except DuplicateKeyError:
        return JSONResponse(
            status_code=409,
            content={"status": False, "message": "UAV with this serial number already exists."}
        )
    except Exception as e:
        logger.error("Error adding UAV: %s", e, exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"status": False, "message": "An error occurred while adding the UAV."}
        )
