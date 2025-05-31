from typing import Self
from pydantic import BaseModel, EmailStr, Field, model_validator
from pydantic_extra_types.phone_numbers import PhoneNumber

class UserRegistrationScheme(BaseModel):
    login: str = Field(..., min_length=3, max_length=32, description="Unique username for registration", examples=["new_user", "test_account"])
    mail: EmailStr = Field(..., description="Valid email address of the user", examples=["examplex@example.ru", "zxc@zxc.ru"])
    phone: PhoneNumber = Field(..., description="User's phone number in international format", examples=["+1234567890", "+9876543210"])
    password: str = Field(..., min_length=8, description="Password with at least 8 characters", examples=["P@ssw0rd123", "SecurePass456"])
    repetition_password: str = Field(..., min_length=8, exclude=True, description="Repeat of the password to confirm", examples=["P@ssw0rd123", "SecurePass456"])

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.repetition_password:
            raise ValueError('Passwords do not match')
        return self

    class Config:
        title = "UserRegistration"
        schema_extra = {
            "example": {
                "login": "new_user",
                "mail": "user@example.com",
                "phone": "+1234567890",
                "password": "P@ssw0rd123",
                "repetition_password": "P@ssw0rd123"
            }
        }