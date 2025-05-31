from pydantic import BaseModel, Field, field_validator
import re

class UavDeleteScheme(BaseModel):
    serial_number: str = Field(..., min_length=1, max_length=32, description="Serial number of the UAV to delete", examples=["1234-5678", "8765-4321"])
    reason: str = Field(..., min_length=1, max_length=256, description="Reason for deleting the UAV", examples=["Износ батареи", "Устаревшая модель", "Потеря связи с аппаратом"])

    @field_validator("serial_number", mode='before')
    def validate_serial_number(cls, v: str) -> str:
        if not re.fullmatch(r"\d{4}-\d{4}", v):
            raise ValueError("serial_number must be in format 0000-0000")
        return v

    class Config:
        title = "UavDelete"
        schema_extra = {
            "example": {
                "serial_number": "1234-5678",
                "reason": "Износ батареи"
            }
        }