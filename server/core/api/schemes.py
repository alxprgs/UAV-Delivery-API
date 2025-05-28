from typing_extensions import Self
from decimal import Decimal
import re

from fastapi import Query
from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from server.core.config import settings
from server.core.functions.hash import create_hash


class UserRegistration(BaseModel):
    login: str = Field(..., max_length=32, min_length=3, description="Unique username for registration")
    mail: EmailStr = Field(..., description="Valid email address of the user")
    phone: PhoneNumber = Field(..., description="User's phone number in international format")
    password: str = Field(..., min_length=8, description="Password with at least 8 characters")
    repetition_password: str = Field(..., min_length=8, description="Repeat of the password to confirm")

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.repetition_password:
            raise ValueError('Passwords do not match')
        return self

class UserRootCreate(BaseModel):
    login: str = Field(..., description="Login of the root user")
    mail: EmailStr = Field(..., description="Email address of the root user")
    phone: PhoneNumber = Field(..., description="Phone number of the root user")
    password: str = Field(..., description="Hashed password of the root user")

    @classmethod
    def create(cls) -> "UserRootCreate":
        hashed_password = create_hash(settings.ROOTUSER_PASSWORD)
        return cls(
            login="root",
            mail="proshka20081010@gmail.com",
            phone="+79933481536",
            password=hashed_password
        )

class UserAuthorization(BaseModel):
    login: str = Field(..., max_length=32, min_length=3, description="User login for authentication")
    password: str = Field(..., min_length=4, description="User password for authentication")

class UserSetPermission(BaseModel):
    value: bool = Query(..., description="New value of the permission (true or false)")
    permission: str = Query(..., min_length=1, description="Name of the permission to change or set")
    login: str = Query(..., min_length=4, max_length=32, description="User login")

class CreateOrder(BaseModel):
    coordinates: str = Field(..., description="Coordinates in 'lat,lon' format")
    delivered: dict = Field(..., description="Delivery facilities with item names as keys and their costs as values")
    cost_delivered: float = Field(default=0, description="Cost of delivery in rubles (calculated automatically)")

    @field_validator("coordinates")
    def parse_coordinates(cls, v):
        try:
            lat, lon = v.split(",")
            return (float(lat), float(lon))
        except Exception:
            raise ValueError("Use 'lat,lon' format")

    @model_validator(mode='after')
    def calculate_cost_delivered(self) -> Self:
        self.cost_delivered = sum(Decimal(v) for v in self.delivered.values())
        return self
    
class AddUAVScheme(BaseModel):
    name: str = Field(..., min_length=1, max_length=32, description="Name of the UAV")
    location: str = Field(..., min_length=1, max_length=32, description="Current location of the UAV")
    max_weight: float = Field(..., gt=0, description="Maximum weight the UAV can carry in kg")
    max_speed: float = Field(..., gt=0, description="Maximum speed of the UAV in km/h")
    serial_number: str = Field(..., min_length=1, max_length=32, description="Serial number of the UAV")
    battery_capacity: float = Field(..., gt=0, description="Battery capacity of the UAV in mAh")
    battery_voltage: float = Field(..., gt=0, description="Battery voltage of the UAV in V")
    battery_charge: float = Field(..., ge=0, description="Current battery charge of the UAV in mAh")
    battery_status: bool = Field(..., description="True if battery is installed, False if not")

    @field_validator("serial_number")
    def validate_serial_number(cls, v):
        if not re.fullmatch(r"\d{4}-\d{4}", v):
            raise ValueError("serial_number must be in format 0000-0000")
        return v

class AddBaseScheme(BaseModel):
    name: str = Field(..., min_length=1, max_length=32, description="Name of the base")
    location: str = Field(..., min_length=1, max_length=32, description="Location of the base")
    max_uavs: int = Field(..., gt=0, description="Maximum number of UAVs that can be at the base at the same time")
    max_uav_weight: float = Field(..., gt=0, description="Maximum weight of UAVs that can be at the base at the same time in kg")