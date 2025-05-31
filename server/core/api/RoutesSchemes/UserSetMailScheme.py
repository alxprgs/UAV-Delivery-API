from pydantic import BaseModel, Field, EmailStr

class UserSetMailScheme(BaseModel):
    login: str = Field(..., min_length=4, max_length=32, description="Login of the user whose email is being set", examples=["operator1", "admin_user"])
    mail: EmailStr = Field(..., description="New email address", examples=["examplex@example.ru", "zxc@zxc.ru"])
    reason: str = Field(..., min_length=1, max_length=256, description="Reason for changing the email address", examples=["Смена корпоративного адреса", "Обновление контактной информации"])
    access_token: str = Field(..., description="Access token for changing the email address", examples=["eyJhbGciOiJIUzI1Ni..."])

    class Config:
        title = "UserSetMail"
        schema_extra = {
            "example": {
                "login": "operator1",
                "mail": "newmail@example.com",
                "reason": "Смена корпоративного адреса",
                "access_token": "eyJhbGciOiJIUzI1Ni..."
            }
        }