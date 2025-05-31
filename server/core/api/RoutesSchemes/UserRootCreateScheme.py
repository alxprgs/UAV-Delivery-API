from pydantic import BaseModel, Field, EmailStr
from pydantic_extra_types.phone_numbers import PhoneNumber

class UserRootCreateScheme(BaseModel):
    login: str = Field(..., description="Login of the root user", min_length=4, max_length=32, examples=["root", "admin"])
    mail: EmailStr = Field(..., description="Email address of the root user", examples=["examplex@example.ru", "zxc@zxc.ru"])
    phone: PhoneNumber = Field(..., description="Phone number of the root user", examples=["+10000000000", "+1234567890"])
    password: str = Field(..., description="Hashed password of the root user", examples=["$2b$12$XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX", "$2b$12$anotherHashedPasswordExample"])

    class Config:
        title = "UserRootCreate"
        schema_extra = {
            "example": {
                "login": "root",
                "mail": "root@company.com",
                "phone": "+10000000000",
                "password": "$2b$12$XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
            }
        }