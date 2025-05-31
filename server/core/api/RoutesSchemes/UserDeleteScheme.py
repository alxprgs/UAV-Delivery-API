from pydantic import BaseModel, Field

class UserDeleteScheme(BaseModel):
    login: str = Field(..., min_length=4, max_length=32, description="Login of the user to delete", examples=["operator1", "admin_user"])
    reason: str = Field(..., min_length=1, max_length=256, description="Reason for deleting the user", examples=["Уволен по собственному желанию", "Нарушение корпоративной политики"])

    class Config:
        title = "UserDelete"
        schema_extra = {
            "example": {
                "login": "operator1",
                "reason": "Уволен по собственному желанию"
            }
        }