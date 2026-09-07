from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.models.activity import DailyActivity
from app.schemas.activity import ActivityCreate, ActivityOut
from app.schemas.plan import PlanOut, AnalysisOut
from app.services.auth_service import get_current_user
from app.services.fitness_service import save_activity_and_generate_plan

router = APIRouter(prefix="/activity", tags=["activity"])


@router.post("", response_model=dict)
def create_activity(
    payload: ActivityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    allowed_intensity = {"light", "moderate", "high"}
    allowed_feeling = {"tired", "normal", "energetic"}
    if payload.exercise_intensity not in allowed_intensity:
        raise HTTPException(status_code=400, detail="Invalid intensity")
    if payload.feeling not in allowed_feeling:
        raise HTTPException(status_code=400, detail="Invalid feeling")

    activity, analysis, plan = save_activity_and_generate_plan(
        db, current_user, payload.model_dump()
    )
    return {
        "activity": ActivityOut.model_validate(activity),
        "analysis": AnalysisOut(
            activity_level=analysis.activity_level,
            fitness_score=analysis.fitness_score,
        ),
        "plan": PlanOut.model_validate(plan),
    }


@router.get("/today", response_model=ActivityOut | None)
def get_today(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from datetime import date

    row = (
        db.query(DailyActivity)
        .filter(DailyActivity.user_id == current_user.id, DailyActivity.date == date.today())
        .first()
    )
    return row


@router.get("/history", response_model=list[ActivityOut])
def history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = (
        db.query(DailyActivity)
        .filter(DailyActivity.user_id == current_user.id)
        .order_by(DailyActivity.date.desc())
        .limit(30)
        .all()
    )
    return rows
