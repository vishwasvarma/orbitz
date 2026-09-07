from datetime import datetime
from sqlalchemy import Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database.connection import Base


class FitnessAnalysis(Base):
    __tablename__ = "fitness_analysis"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    daily_activity_id: Mapped[int] = mapped_column(ForeignKey("daily_activity.id"), unique=True)
    activity_level: Mapped[str] = mapped_column(String(32))
    fitness_score: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    activity = relationship("DailyActivity", back_populates="analysis")
