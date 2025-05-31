from pydantic import BaseModel, Field, field_validator, model_validator
from typing import Tuple, Dict, Self
from decimal import Decimal

class OrderCreateScheme(BaseModel):
    coordinates: Tuple[float, float] = Field(..., description="Coordinates as (lat, lon)", examples=["55.7558,37.6173"])
    delivered: Dict[str, Decimal] = Field(..., description="Delivery items and their costs", examples=[{"package": 120.50, "fragile": 75.00}])
    cost_delivered: Decimal = Field(default=Decimal(0), description="Cost of delivery in rubles (calculated automatically)", examples=["195.50"])

    @field_validator("coordinates", mode='before')
    def parse_coordinates(cls, v: str) -> Tuple[float, float]:
        try:
            lat, lon = v.split(",")
            return (float(lat), float(lon))
        except Exception:
            raise ValueError("Use 'lat,lon' format")

    @model_validator(mode='after')
    def calculate_cost_delivered(self) -> Self:
        total = sum(self.delivered.values())
        self.cost_delivered = total
        return self

    class Config:
        title = "OrderCreate"
        schema_extra = {
            "example": {
                "coordinates": "55.7558,37.6173",
                "delivered": {"package": 120.50, "fragile": 75.00},
            }
        }