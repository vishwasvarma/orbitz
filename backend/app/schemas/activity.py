from datetime import date
from pydantic import BaseModel, Field


class ActivityCreate(BaseModel):
    weight: float = Field(gt=20, lt=400)
    steps: int = Field(ge=0, le=100000)
    exercise_minutes: int = Field(ge=0, le=600)
    exercise_intensity: str
    exercise_types: list[str] = []
    sleep_hours: float = Field(ge=0, le=24)
    water_liters: float = Field(ge=0, le=15)
    sitting_hours: float = Field(ge=0, le=24, default=0)
    feeling: str = "normal"


class ActivityOut(BaseModel):
    id: int
    date: date
    weight: float
    steps: int
    exercise_minutes: int
    exercise_intensity: str
    exercise_types: list
    sleep_hours: float
    water_liters: float
    sitting_hours: float
    feeling: str

    class Config:
        from_attributes = True
