from pydantic import BaseModel, Field, field_validator
from typing import Tuple
import re

class UavAddScheme(BaseModel):
    name: str = Field(..., min_length=1, max_length=32, description="Name of the UAV", examples=["Drone-X1", "SkyWatcher Pro", "Eagle Eye"])
    location: str = Field(..., min_length=1, max_length=32, description="Current location of the UAV", examples=["Hangar 3", "Sector 5", "Zone A1"])
    coordinates: Tuple[float, float] = Field(..., description="Coordinates of the UAV as (lat, lon)", examples=["48.8566,2.3522", "34.0522,-118.2437", "51.5074,-0.1278"])
    max_weight: float = Field(..., gt=0, description="Maximum weight the UAV can carry in kg", examples=[1.5, 3.0, 5.0])
    max_speed: float = Field(..., gt=0, description="Maximum speed of the UAV in km/h", examples=[30.0, 60.0, 100.0])
    serial_number: str = Field(..., min_length=1, max_length=32, description="Serial number of the UAV", examples=["1234-5678", "9876-5432", "0000-1111"])
    battery_capacity: float = Field(..., gt=0, description="Battery capacity of the UAV in mAh", examples=[3000, 5000, 10000])
    battery_voltage: float = Field(..., gt=0, description="Battery voltage of the UAV in V", examples=[11.1, 14.8, 22.2])
    battery_charge: float = Field(..., ge=0, description="Current battery charge of the UAV in mAh", examples=[1500, 2500, 5000])
    battery_status: bool = Field(..., description="True if battery is installed, False if not", examples=[True, False])

    @field_validator("serial_number", mode='before')
    def validate_serial_number(cls, v: str) -> str:
        if not re.fullmatch(r"\d{4}-\d{4}", v):
            raise ValueError("serial_number must be in format 0000-0000")
        return v
    
    @field_validator("coordinates", mode='before')
    def parse_coordinates(cls, v: str) -> Tuple[float, float]:
        try:
            lat, lon = v.split(",")
            return (float(lat), float(lon))
        except Exception:
            raise ValueError("Use 'lat,lon' format")

    class Config:
        title = "UavAdd"
        schema_extra = {
            "example": {
                "name": "Drone-X1",
                "location": "Hangar 3",
                "coordinates": "48.8566,2.3522",
                "max_weight": 3.5,
                "max_speed": 60.0,
                "serial_number": "1234-5678",
                "battery_capacity": 5000,
                "battery_voltage": 11.1,
                "battery_charge": 2500,
                "battery_status": True
            }
        }