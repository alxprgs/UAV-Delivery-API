from pydantic import BaseModel, Field, field_validator
from typing import Tuple
import re

class UavSetDataScheme(BaseModel):
    location: str = Field(..., min_length=1, max_length=32, description="New location of the UAV", examples=["Hangar 5", "Field A", "Maintenance Bay"])
    coordinates: Tuple[float, float] = Field(..., description="New coordinates of the UAV as (lat, lon)", examples=[(40.7128, -74.0060), (34.0522, -118.2437)])
    carryweight: float = Field(..., gt=0, description="New carry weight of the UAV in kg", examples=[2.0, 5.0, 10.0])
    serial_number: str = Field(..., min_length=1, max_length=32, description="Serial number of the UAV to update", examples=["1234-5678", "8765-4321"])
    battery_voltage: float = Field(..., gt=0, description="New battery voltage of the UAV in V", examples=[11.1, 14.8, 22.2])
    battery_charge: float = Field(..., ge=0, description="New current battery charge of the UAV in mAh", examples=[1500, 2500, 5000])
    battery_status: bool = Field(..., description="True if battery is installed, False if not", examples=[True, False])

    @field_validator("serial_number", mode='before')
    def validate_serial_number(cls, v: str) -> str:
        if not re.fullmatch(r"\d{4}-\d{4}", v):
            raise ValueError("serial_number must be in format 0000-0000")
        return v

    class Config:
        title = "UavSetData"
        schema_extra = {
            "example": {
                "location": "Hangar 5",
                "coordinates": "40.7128,74.0060",
                "carryweight": 2.0,
                "serial_number": "1234-5678",
                "battery_voltage": 11.1,
                "battery_charge": 3000,
                "battery_status": False
            }
        }