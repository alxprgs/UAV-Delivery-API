from pydantic import BaseModel, Field

class UserSetPhoneScheme(BaseModel):
    login: str = Field(..., min_length=4, max_length=32, description="Login of the user whose phone is being changed", examples=["operator1", "admin_user"])
    phone: str = Field(..., description="New phone number in international format", examples=["+12345678901", "+9876543210"])
    reason: str = Field(..., min_length=1, max_length=256, description="Reason for changing the phone number", examples=["Обновление контактной информации", "Смена номера по запросу пользователя"])
    access_token: str = Field(..., description="Access token for changing the phone number", examples=["eyJhbGciOiJIUzI1Ni..."])

    class Config:
        title = "UserSetPhone"
        schema_extra = {
            "example": {
                "login": "operator1",
                "phone": "+12345678901",
                "reason": "Обновление по инициативе пользователя",
                "access_token": "eyJhbGciOiJIUzI1Ni..."
            }
        }