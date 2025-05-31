from pydantic import BaseModel, Field

class BaseDeleteScheme(BaseModel):
    name: str = Field(..., min_length=1, max_length=32, description="Name of the base to delete", examples=["Forward Base Alpha", "Main Operations Base"])
    location: str = Field(..., min_length=1, max_length=32, description="Location of the base to delete", examples=["Sector 12", "Zone A1", "Base Camp Bravo"])
    reason: str = Field(..., min_length=1, max_length=256, description="Reason for deleting the base", examples=["База более не используется", "Закрытие по техническим причинам", "Перенос операций на другую базу"])

    class Config:
        title = "BaseDelete"
        schema_extra = {
            "example": {
                "name": "Forward Base Alpha",
                "location": "Sector 12",
                "reason": "База более не используется"
            }
        }