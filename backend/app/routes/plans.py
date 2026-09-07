from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.models.plan import FitnessPlan
from app.schemas.plan import PlanOut
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/plans", tags=["plans"])


@router.get("/tomorrow", response_model=PlanOut | None)
def tomorrow_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    target = date.today() + timedelta(days=1)
    plan = (
        db.query(FitnessPlan)
        .filter(FitnessPlan.user_id == current_user.id, FitnessPlan.date == target)
        .first()
    )
    return plan


@router.get("/history", response_model=list[PlanOut])
def plan_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(FitnessPlan)
        .filter(FitnessPlan.user_id == current_user.id)
        .order_by(FitnessPlan.date.desc())
        .limit(30)
        .all()
    )


@router.get("/{plan_id}", response_model=PlanOut)
def get_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    plan = (
        db.query(FitnessPlan)
        .filter(FitnessPlan.id == plan_id, FitnessPlan.user_id == current_user.id)
        .first()
    )
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan
