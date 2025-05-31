from pydantic import BaseModel, Field, model_validator
from typing import Self

class UserSetPasswordByAdminScheme(BaseModel):
    login: str = Field(..., min_length=4, max_length=32, description="Login of the user whose password is being set", examples=["operator1", "admin_user"]) 
    new_password: str = Field(..., min_length=8, description="New password for the user", examples=["AdminReset123", "SecurePass456"])
    repetition_new_password: str = Field(..., min_length=8, exclude=True, description="Repeat of the new password to confirm", examples=["AdminReset123", "SecurePass456"])
    reason: str = Field(..., min_length=1, max_length=256, description="Reason for changing the password", examples=["Административный сброс пароля", "Смена по запросу пользователя"])

    @model_validator(mode='after')
    def check_new_passwords_match(self) -> Self:
        if self.new_password != self.repetition_new_password:
            raise ValueError('New passwords do not match')
        return self

    class Config:
        title = "UserSetPasswordByAdmin"
        schema_extra = {
            "example": {
                "login": "operator1",
                "new_password": "AdminReset123",
                "repetition_new_password": "AdminReset123",
                "reason": "Административный сброс пароля"
            }
        }