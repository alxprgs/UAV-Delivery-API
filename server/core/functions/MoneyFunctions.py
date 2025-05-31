from server.core.api.FunctionsSchemes.PaymentCreateScheme import PaymentCreateScheme
from server.core.api.FunctionsSchemes.MoneyGetScheme import MoneyGetScheme
from server.core.functions.MongoDBFunctions import GetString
from server.core.Config import settings
from server import db
from uuid import uuid4
from decimal import Decimal, ROUND_HALF_UP
from server.core.LoggingModule import logger
import asyncio
from yookassa import Payment, Configuration


async def PaymentCreate(data: PaymentCreateScheme) -> dict | None:
    if not settings.YOOKASSA_SHOP_ID or not settings.YOOKASSA_SECRET_KEY:
        logger.error("YooKassa credentials are not set.")
        return None

    order_id = str(uuid4())
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

    payment_data = {
        "amount": {
            "value": f"{data.amount:.2f}",
            "currency": data.currency
        },
        "confirmation": {
            "type": "redirect",
            "return_url": f"https://{settings.DOMAIN}/v1/orders/return_payment"
        },
        "capture": True,
        "description": f"Order {order_id}",
        "receipt": {
            "customer": data.mail,
            "items": data.items
        }
    }

    def validate_payment_data(data_dict: dict):
        for item in data_dict["receipt"]["items"]:
            val = Decimal(item["amount"]["value"]).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            if val <= 0:
                raise ValueError(f"Invalid amount for '{item['description']}': {val}")
            item["amount"]["value"] = f"{val:.2f}"

            qty = Decimal(item.get("quantity", "1")).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)
            if qty <= 0:
                raise ValueError(f"Invalid quantity for '{item['description']}': {qty}")
            item["quantity"] = f"{qty:.3f}"

    try:
        validate_payment_data(payment_data)
    except ValueError as e:
        logger.error("Validation error in payment data: %s", str(e), exc_info=True)
        return None

    try:
        payment = await asyncio.get_event_loop().run_in_executor(
            None, lambda: Payment.create(payment_data)
        )
        return payment.to_dict()
    except Exception as e:
        logger.error("Payment creation failed: %s", str(e), exc_info=True)
        return None

async def MoneyGet(data: MoneyGetScheme) -> float | None:
    money = await GetString(database=db, field="login", collection="users", search=data.login, get_field="money")
    return float(money) if money is not None else None

async def MoneySet() -> bool:
    logger.error("MoneySet function is not implemented.")
    return False

async def MoneyAdd() -> bool:
    logger.error("MoneyAdd function is not implemented.")
    return False

async def MoneyRemove() -> bool:
    logger.error("MoneyRemove function is not implemented.")
    return False

async def MoneyTransfer() -> bool:
    logger.error("MoneyTransfer function is not implemented.")
    return False

