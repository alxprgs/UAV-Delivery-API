from typing import Self, Tuple, Dict
from decimal import Decimal
import re

from fastapi import Query
from pydantic import BaseModel, EmailStr, Field, model_validator, field_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

from server.core.config import settings
from server.core.functions.hash import create_hash

class UserRegistration(BaseModel):
    login: str = Field(..., min_length=3, max_length=32, description="Unique username for registration")
    mail: EmailStr = Field(..., description="Valid email address of the user")
    phone: PhoneNumber = Field(..., description="User's phone number in international format")
    password: str = Field(..., min_length=8, description="Password with at least 8 characters")
    repetition_password: str = Field(..., min_length=8, exclude=True, description="Repeat of the password to confirm")

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
    login: str = Field(..., min_length=3, max_length=32, description="User login for authentication")
    password: str = Field(..., min_length=4, description="User password for authentication")


class UserSetPermission(BaseModel):
    value: bool = Field(..., description="New value of the permission (true or false)")
    permission: str = Field(..., min_length=1, description="Name of the permission to change or set")
    login: str = Field(..., min_length=4, max_length=32, description="User login")
    reason: str = Field(..., min_length=1, max_length=256, description="Reason for changing the permission")

class UserDelete(BaseModel):
    login: str = Field(..., min_length=4, max_length=32, description="Login of the user to delete")
    reason: str = Field(..., min_length=1, max_length=256, description="Reason for deleting the user")

class UserChangePassword(BaseModel):
    login: str = Field(..., min_length=4, max_length=32, description="Login of the user whose password is being changed")
    old_password: str = Field(..., min_length=4, description="Current password of the user")
    new_password: str = Field(..., min_length=8, description="New password for the user")
    repetition_new_password: str = Field(..., min_length=8, exclude=True, description="Repeat of the new password to confirm")
    access_token: str = Field(..., description="Access token for changing the password")

    @model_validator(mode='after')
    def check_new_passwords_match(self) -> Self:
        if self.new_password != self.repetition_new_password:
            raise ValueError('New passwords do not match')
        return self

class UserSetPhone(BaseModel):
    login: str = Field(..., min_length=4, max_length=32, description="Login of the user whose phone is being set")
    phone: PhoneNumber = Field(..., description="New phone number in international format")
    reason: str = Field(..., min_length=1, max_length=256, description="Reason for changing the phone number")
    access_token: str = Field(..., description="Access token for changing the phone number")

class UserSetMail(BaseModel):
    login: str = Field(..., min_length=4, max_length=32, description="Login of the user whose email is being set")
    mail: EmailStr = Field(..., description="New email address")
    reason: str = Field(..., min_length=1, max_length=256, description="Reason for changing the email address")
    access_token: str = Field(..., description="Access token for changing the email address")

class UserSetPasswordByAdmin(BaseModel):
    login: str = Field(..., min_length=4, max_length=32, description="Login of the user whose password is being set")
    new_password: str = Field(..., min_length=8, description="New password for the user")
    repetition_new_password: str = Field(..., min_length=8, exclude=True, description="Repeat of the new password to confirm")
    reason: str = Field(..., min_length=1, max_length=256, description="Reason for changing the password")

    @model_validator(mode='after')
    def check_new_passwords_match(self) -> Self:
        if self.new_password != self.repetition_new_password:
            raise ValueError('New passwords do not match')
        return self

class CreateOrder(BaseModel):
    coordinates: Tuple[float, float] = Field(..., description="Coordinates as (lat, lon)")
    delivered: Dict[str, Decimal] = Field(..., description="Delivery items and their costs")
    cost_delivered: Decimal = Field(default=Decimal(0), description="Cost of delivery in rubles (calculated automatically)")

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

    @field_validator("serial_number", mode='before')
    def validate_serial_number(cls, v: str) -> str:
        if not re.fullmatch(r"\d{4}-\d{4}", v):
            raise ValueError("serial_number must be in format 0000-0000")
        return v

class AddBaseScheme(BaseModel):
    name: str = Field(..., min_length=1, max_length=32, description="Name of the base")
    location: str = Field(..., min_length=1, max_length=32, description="Location of the base")
    max_uavs: int = Field(..., gt=0, description="Maximum number of UAVs that can be at the base at the same time")
    max_uav_weight: float = Field(..., gt=0, description="Maximum weight of UAVs that can be at the base at the same time in kg")

class DeleteBaseScheme(BaseModel):
    name: str = Field(..., min_length=1, max_length=32, description="Name of the base to delete")
    location: str = Field(..., min_length=1, max_length=32, description="Location of the base to delete")
    reason: str = Field(..., min_length=1, max_length=256, description="Reason for deleting the base")

class DeleteUAVScheme(BaseModel):
    serial_number: str = Field(..., min_length=1, max_length=32, description="Serial number of the UAV to delete")
    reason: str = Field(..., min_length=1, max_length=256, description="Reason for deleting the UAV")

    @field_validator("serial_number", mode='before')
    def validate_serial_number(cls, v: str) -> str:
        if not re.fullmatch(r"\d{4}-\d{4}", v):
            raise ValueError("serial_number must be in format 0000-0000")
        return v