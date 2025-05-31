from pydantic import BaseModel, Field

class BaseAddScheme(BaseModel):
    name: str = Field(..., min_length=1, max_length=32, description="Name of the base", examples=["Forward Base Alpha", "Main Operations Base"])
    location: str = Field(..., min_length=1, max_length=32, description="Location of the base", examples=["Sector 12", "Zone A1", "Base Camp Bravo"])
    max_uavs: int = Field(..., gt=0, description="Maximum number of UAVs that can be at the base at the same time", examples=[5, 10, 20])
    max_uav_weight: float = Field(..., gt=0, description="Maximum weight of UAVs that can be at the base at the same time in kg", examples=[12.5, 25.0, 50.0])

    class Config:
        title = "BaseAdd"
        schema_extra = {
            "example": {
                "name": "Forward Base Alpha",
                "location": "Sector 12",
                "max_uavs": 5,
                "max_uav_weight": 12.5
            }
        }