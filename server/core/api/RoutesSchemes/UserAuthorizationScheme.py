from pydantic import BaseModel, Field

class UserAuthorizationScheme(BaseModel):
    login: str = Field(..., min_length=3, max_length=32, description="User login for authentication", examples=["operator1", "admin_user"])
    password: str = Field(..., min_length=4, description="User password for authentication", examples=["strongP@ssw0rd", "anotherSecurePass123"])

    class Config:
        title = "UserAuth"
        schema_extra = {
            "example": {
                "login": "operator1",
                "password": "strongP@ssw0rd"
            }
        }