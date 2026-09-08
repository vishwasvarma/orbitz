from datetime import date
from pydantic import BaseModel, Field, field_validator


class ActivityCreate(BaseModel):
    weight: float = Field(gt=20, lt=400)
    steps: int = Field(ge=0, le=100000)
    exercise_minutes: int | None = Field(default=None, ge=0, le=600)
    exercise_intensity: str
    exercise_types: list[str] = []
    exercise_breakdown: dict[str, int] = {}
    sleep_hours: float = Field(ge=0, le=24)
    water_liters: float = Field(ge=0, le=15)
    sitting_hours: float = Field(ge=0, le=24, default=0)
    feeling: str = "normal"
    medical_constraints: list[str] = []
    diet_preference: str
    food_allergies: list[str] = []

    @field_validator("exercise_breakdown", mode="before")
    @classmethod
    def coerce_breakdown(cls, value):
        if not value:
            return {}
        cleaned = {}
        for key, minutes in dict(value).items():
            name = str(key).strip()
            if not name:
                continue
            try:
                mins = int(minutes)
            except (TypeError, ValueError):
                continue
            if mins > 0:
                cleaned[name] = min(mins, 600)
        return cleaned

    @field_validator("food_allergies", "medical_constraints", "exercise_types", mode="before")
    @classmethod
    def coerce_str_list(cls, value):
        if not value:
            return []
        return [str(item).strip() for item in value if str(item).strip()]


class ActivityOut(BaseModel):
    id: int
    date: date
    weight: float
    steps: int
    exercise_minutes: int
    exercise_intensity: str
    exercise_types: list
    exercise_breakdown: dict = {}
    sleep_hours: float
    water_liters: float
    sitting_hours: float
    feeling: str
    medical_constraints: list = []
    diet_preference: str | None = None
    food_allergies: list = []

    class Config:
        from_attributes = True

    @field_validator("exercise_breakdown", mode="before")
    @classmethod
    def default_breakdown(cls, value):
        return value or {}

    @field_validator("medical_constraints", "food_allergies", "exercise_types", mode="before")
    @classmethod
    def default_list(cls, value):
        return value or []
