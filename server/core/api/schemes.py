from typing_extensions import Self

from fastapi import Query
from pydantic import BaseModel, EmailStr, Field, model_validator
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
