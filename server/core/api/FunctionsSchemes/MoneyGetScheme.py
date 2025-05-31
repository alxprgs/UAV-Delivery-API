from pydantic import BaseModel, Field

class MoneyGetScheme(BaseModel):
    login: str = Field(..., min_length=4, max_length=32, description="Login of the user whose nickname is being retrieved", examples=["operator1", "admin_user"])

    class Config:
        json_schema_extra = {
            "example": {
                "Nickname": "user123"
            }
        }