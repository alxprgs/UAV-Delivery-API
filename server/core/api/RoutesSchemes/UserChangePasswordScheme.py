from pydantic import BaseModel, Field, model_validator
from typing import Self

class UserChangePasswordScheme(BaseModel):
    login: str = Field(..., min_length=4, max_length=32, description="Login of the user whose password is being changed", examples=["operator1", "admin_user"])
    old_password: str = Field(..., min_length=4, description="Current password of the user", examples=["oldP@ss1", "currentSecurePass123"])
    new_password: str = Field(..., min_length=8, description="New password for the user", examples=["newStrongP@ss2", "anotherSecurePass456"])
    repetition_new_password: str = Field(..., min_length=8, exclude=True, description="Repeat of the new password to confirm", examples=["newStrongP@ss2", "anotherSecurePass456"])
    access_token: str = Field(..., description="Access token for changing the password", examples=["eyJhbGciOiJIUzI1Ni..."])

    @model_validator(mode='after')
    def check_new_passwords_match(self) -> Self:
        if self.new_password != self.repetition_new_password:
            raise ValueError('New passwords do not match')
        return self

    class Config:
        title = "UserChangePassword"
        schema_extra = {
            "example": {
                "login": "operator1",
                "old_password": "oldP@ss1",
                "new_password": "newStrongP@ss2",
                "repetition_new_password": "newStrongP@ss2",
                "access_token": "eyJhbGciOiJIUzI1Ni..."
            }
        }