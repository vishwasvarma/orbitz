from datetime import date
from pydantic import BaseModel


class PlanOut(BaseModel):
    id: int
    date: date
    plan: dict
    reason: str

    class Config:
        from_attributes = True


class AnalysisOut(BaseModel):
    activity_level: str
    fitness_score: float
