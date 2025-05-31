from pydantic import BaseModel, Field

class UserSetPermissionScheme(BaseModel):
    value: bool = Field(..., description="New value of the permission (true or false)", examples=[True, False])
    permission: str = Field(..., min_length=1, description="Name of the permission to change or set", examples=["can_fly_over_restricted", "can_access_confidential_data"])
    login: str = Field(..., min_length=4, max_length=32, description="User login", examples=["operator1", "admin_user"])
    reason: str = Field(..., min_length=1, max_length=256, description="Reason for changing the permission", examples=["Расширение зоны операций", "Обновление доступа к данным"])

    class Config:
        title = "UserSetPermission"
        schema_extra = {
            "example": {
                "value": True,
                "permission": "can_fly_over_restricted",
                "login": "operator1",
                "reason": "Расширение зоны операций"
            }
        }