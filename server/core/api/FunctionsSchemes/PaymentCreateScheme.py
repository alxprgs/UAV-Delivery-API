from decimal import Decimal
from typing import List
from pydantic import BaseModel, Field, model_validator, EmailStr

class PaymentItemScheme(BaseModel):
    description: str = Field(..., min_length=1, max_length=256, description="Item description", examples=["Product A", "Service Fee"])
    quantity: Decimal = Field(..., gt=0, description="Quantity of the item (must be > 0)", examples=["1", "2"])
    amount: Decimal = Field(..., gt=0, description="Amount per item in cents (must be > 0)", examples=["3000", "1500.75"])
    vat_code: int = Field(..., ge=1, le=6, description="VAT code (usually from 1 to 6)", examples=[1, 2, 3, 4, 5, 6])

    class Config:
        json_schema_extra = {
            "example": {
                "description": "Product A",
                "quantity": "2",
                "amount": "5000",
                "vat_code": 2
            }
        }

class PaymentCreateScheme(BaseModel):
    amount: Decimal = Field(..., gt=0, description="Total amount in cents to be charged", examples=["10000", "2500.50"])
    description: str = Field(..., min_length=1, max_length=256, description="Description of the payment", examples=["Payment for order #12345", "Service fee"])
    mail: EmailStr = Field(..., description="Email address for sending the receipt", examples=["examplex@example.ru", "zxc@zxc.ru"])
    currency: str = Field(
        default="RUB",
        regex=r"^[A-Z]{3}$",
        description="Currency code in ISO 4217 format (default is RUB)"
    )
    items: List[PaymentItemScheme] = Field(
        default_factory=list,
        description="List of items in the receipt"
    )

    @model_validator(mode="after")
    def validate_model(self) -> "PaymentCreateScheme":
        supported_currencies = {"RUB", "USD", "EUR"}
        if self.currency not in supported_currencies:
            raise ValueError(f"Unsupported currency. Only {', '.join(supported_currencies)} are allowed.")

        items_total = sum(item.amount * item.quantity for item in self.items)
        if items_total != self.amount:
            raise ValueError(f"Sum of items (amount*quantity = {items_total}) does not match total amount ({self.amount})")

        return self

    class Config:
        json_schema_extra = {
            "example": {
                "amount": "10000",
                "description": "Payment for order #12345",
                "currency": "RUB",
                "items": [
                    {
                        "description": "Product A",
                        "quantity": "1",
                        "amount": "3000",
                        "vat_code": 2
                    },
                    {
                        "description": "Product B",
                        "quantity": "2",
                        "amount": "3500",
                        "vat_code": 2
                    }
                ]
            }
        }
