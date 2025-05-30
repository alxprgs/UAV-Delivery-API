from fastapi import Request, HTTPException, status
from server import app, db
from fastapi.responses import JSONResponse
from server.core.config import settings
from server.core.functions.mongodb import get_user
from server.core.api.schemes import CreateOrder
from geopy.distance import geodesic
from yookassa import Payment, Configuration
from decimal import Decimal, ROUND_HALF_UP
from server.core.logging import logger
import uuid
import asyncio
import datetime

AIRPORTS = {
    "SVO": (55.981384, 37.412357),
    "DME": (55.413539, 37.901289),
    "VKO": (55.603952, 37.274554)
}

#Обновить в скорейшем времени, всё еще надо
@app.post(
    "/v1/orders/create_order",
    tags=["orders", "post"],
    openapi_extra={"requestBody": {"content": {"application/json": {
                    "example": {
                        "coordinates": "55.7558, 37.6173",
                        "delivered": {
                            "iPhone 14": "79990.00",
                            "MacBook Air": "119990.00"
                        },
                        "cost_delivered": "0"}}}}}, summary="Create Order", description="Creates a new order for delivery based on user coordinates and items to be delivered.")
async def create_order(request: Request, data: CreateOrder):
    if not settings.YOOKASSA_SHOP_ID or not settings.YOOKASSA_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Yookassa credentials are not configured")
    if not data.coordinates or not data.delivered or not data.cost_delivered:
        raise HTTPException(status_code=400, detail="Invalid input data. Coordinates, delivered items, and cost delivered are required.")
    if not isinstance(data.coordinates, tuple) or len(data.coordinates) != 2:
        raise HTTPException(status_code=400, detail="Coordinates must be a tuple of (latitude, longitude).")
    user = await get_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    lat, lon = data.coordinates
    nearest = min(AIRPORTS, key=lambda a: geodesic((lat, lon), AIRPORTS[a]).kilometers)
    raw_distance = geodesic((lat, lon), AIRPORTS[nearest]).kilometers

    distance = (Decimal(raw_distance) * Decimal('1.15')).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    cost = (distance * Decimal(100)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP) * 2
    delivery_fee = ((cost + Decimal(data.cost_delivered)) * Decimal("0.15")).quantize(Decimal("0.01"))

    order_id = str(uuid.uuid4())

    if not settings.YOOKASSA_SHOP_ID or not settings.YOOKASSA_SECRET_KEY:
        raise HTTPException(status_code=500, detail="Yookassa credentials are not configured")

    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

    delivered_items_cost = sum(Decimal(price) for price in data.delivered.values())
    final_cost = (cost + delivery_fee + delivered_items_cost).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    receipt_customer = {}
    if email := user.get("mail"):
        receipt_customer["email"] = email
    if phone := user.get("phone"):
        receipt_customer["phone"] = ''.join(filter(str.isdigit, phone))

    items = []
    items.append({
        "description": f"Delivery to coordinates ({lat:.6f}, {lon:.6f}) from {nearest} airport",
        "quantity": "1.000",
        "amount": {"value": f"{cost:.2f}", "currency": "RUB"},
        "vat_code": 1
    })
    for item_name, price in data.delivered.items():
        items.append({
            "description": f"Delivered item: {item_name}",
            "quantity": "1.000",
            "amount": {"value": f"{Decimal(price):.2f}", "currency": "RUB"},
            "vat_code": 1
        })
    items.append({
        "description": "Delivery fee",
        "quantity": "1.000",
        "amount": {"value": f"{delivery_fee:.2f}", "currency": "RUB"},
        "vat_code": 1
    })

    payment_data = {
        "amount": {"value": f"{final_cost:.2f}", "currency": "RUB"},
        "confirmation": {"type": "redirect", "return_url": f"https://{settings.DOMAIN}/v1/orders/return_payment"},
        "capture": True,
        "description": f"Order {order_id}",
        "receipt": {"customer": receipt_customer, "items": items}
    }

    def validate_payment_data(data_dict):
        for it in data_dict["receipt"]["items"]:
            val = Decimal(it["amount"]["value"]).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if val <= 0:
                raise ValueError(f"Invalid amount for '{it['description']}': {val}")
            it["amount"]["value"] = f"{val:.2f}"
            qty = Decimal(it.get("quantity", "1")).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
            if qty <= 0:
                raise ValueError(f"Invalid quantity for '{it['description']}': {qty}")
            it["quantity"] = f"{qty:.3f}"

    try:
        validate_payment_data(payment_data)
    except ValueError as e:
        logger.error("Validation error in payment data: %s", str(e), exc_info=True)
        raise HTTPException(status_code=400, detail=f"Invalid payment data: {e}")

    try:
        payment = await asyncio.get_event_loop().run_in_executor(None, lambda: Payment.create(payment_data))
    except Exception as e:
        logger.error("Payment creation failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Error creating payment")

    try:
        await db["users"].find_one_and_update(
            {"login": user["login"]},
            {"$push": {"orders": {"payment_id": payment.id}}}
        )
        await db["orders"].insert_one({
            "order_id": order_id,
            "nearest_airport": nearest,
            "distance_km": float(distance),
            "cost": float(final_cost),
            "payment_id": payment.id,
            "created_at": datetime.datetime.utcnow(),
            "status": "pending",
            "user_id": user["_id"],
            "delivered_items": data.delivered,
            "cost_delivered": data.cost_delivered,
            "coordinates": data.coordinates,
            "payment_url": payment.confirmation.confirmation_url
        })
    except Exception as e:
        logger.error("Database update failed: %s", str(e), exc_info=True)
        raise HTTPException(status_code=500, detail="Error saving order")

    return JSONResponse(
        content={
            "message": "Order created successfully.",
            "order_id": order_id,
            "nearest_airport": nearest,
            "distance_km": float(distance),
            "cost": float(final_cost),
            "payment_url": payment.confirmation.confirmation_url
        },
        status_code=status.HTTP_201_CREATED
    )
