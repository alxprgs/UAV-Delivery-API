from pydantic import BaseModel, Field, EmailStr, model_validator
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing_extensions import Self
from server.core.functions.hash import create_hash
from server.core.config import settings

class UserRegistration(BaseModel):
    login: str = Field(..., max_length=32, min_length=3)
    mail: EmailStr
    phone: PhoneNumber
    password: str = Field(..., min_length=8)
    repetition_password: str = Field(..., min_length=8)

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.repetition_password:
            raise ValueError('Passwords do not match')
        return self

class UserRootCreate(BaseModel):
    login: str
    mail: EmailStr
    phone: PhoneNumber
    password: str

    @classmethod
    async def create(cls) -> "UserRootCreate":
        hashed_password = await create_hash(settings.ROOTUSER_PASSWORD)
        return cls(
            login="root",
            mail="proshka20081010@gmail.com",
            phone="+79933481536",
            password=hashed_password
        )

class UserLogin(BaseModel):
    login: str = Field(..., max_length=32, min_length=3)
    password: str = Field(..., min_length=8)
