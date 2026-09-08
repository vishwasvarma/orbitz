from datetime import datetime, date
from sqlalchemy import String, Integer, Float, DateTime, Date, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base


class DailyActivity(Base):
    __tablename__ = "daily_activity"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    weight: Mapped[float] = mapped_column(Float)
    steps: Mapped[int] = mapped_column(Integer)
    exercise_minutes: Mapped[int] = mapped_column(Integer)
    exercise_intensity: Mapped[str] = mapped_column(String(32))
    exercise_types: Mapped[list] = mapped_column(JSON, default=list)
    sleep_hours: Mapped[float] = mapped_column(Float)
    water_liters: Mapped[float] = mapped_column(Float)
    sitting_hours: Mapped[float] = mapped_column(Float, default=0)
    feeling: Mapped[str] = mapped_column(String(32), default="normal")
    exercise_breakdown: Mapped[dict | None] = mapped_column(JSON, nullable=True, default=dict)
    medical_constraints: Mapped[list | None] = mapped_column(JSON, nullable=True, default=list)
    diet_preference: Mapped[str | None] = mapped_column(String(32), nullable=True)
    food_allergies: Mapped[list | None] = mapped_column(JSON, nullable=True, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="activities")
    analysis = relationship("FitnessAnalysis", back_populates="activity", uselist=False)
