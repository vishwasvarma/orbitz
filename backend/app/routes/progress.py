from datetime import date, timedelta
from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user import User
from app.models.activity import DailyActivity
from app.models.analysis import FitnessAnalysis
from app.services.auth_service import get_current_user
from app.services.report_service import build_three_day_pdf, build_weekly_pdf

router = APIRouter(prefix="/progress", tags=["progress"])


@router.get("/weekly")
def weekly(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    start = date.today() - timedelta(days=6)
    activities = (
        db.query(DailyActivity)
        .filter(DailyActivity.user_id == current_user.id, DailyActivity.date >= start)
        .order_by(DailyActivity.date.asc())
        .all()
    )
    if not activities:
        return {
            "days": [],
            "averages": {
                "steps": 0,
                "exercise_minutes": 0,
                "sleep_hours": 0,
                "water_liters": 0,
                "fitness_score": 0,
            },
            "consistency": "0/7",
        }

    scores = []
    for a in activities:
        if a.analysis:
            scores.append(a.analysis.fitness_score)
        else:
            analysis = (
                db.query(FitnessAnalysis)
                .filter(FitnessAnalysis.daily_activity_id == a.id)
                .first()
            )
            if analysis:
                scores.append(analysis.fitness_score)

    n = len(activities)
    return {
        "days": [
            {
                "date": str(a.date),
                "steps": a.steps,
                "exercise_minutes": a.exercise_minutes,
                "sleep_hours": a.sleep_hours,
                "water_liters": a.water_liters,
                "weight": a.weight,
                "fitness_score": a.analysis.fitness_score if a.analysis else None,
            }
            for a in activities
        ],
        "averages": {
            "steps": round(sum(a.steps for a in activities) / n),
            "exercise_minutes": round(sum(a.exercise_minutes for a in activities) / n, 1),
            "sleep_hours": round(sum(a.sleep_hours for a in activities) / n, 1),
            "water_liters": round(sum(a.water_liters for a in activities) / n, 1),
            "fitness_score": round(sum(scores) / len(scores), 1) if scores else 0,
        },
        "consistency": f"{n}/7",
    }


@router.get("/weekly.pdf")
def weekly_pdf(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pdf_bytes = build_weekly_pdf(db, current_user)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="orbitz-weekly-report.pdf"'},
    )


@router.get("/three-day.pdf")
def three_day_pdf(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pdf_bytes = build_three_day_pdf(db, current_user)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": 'attachment; filename="orbitz-3-day-report.pdf"'},
    )


@router.get("/monthly")
def monthly(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    start = date.today() - timedelta(days=29)
    activities = (
        db.query(DailyActivity)
        .filter(DailyActivity.user_id == current_user.id, DailyActivity.date >= start)
        .order_by(DailyActivity.date.asc())
        .all()
    )
    return {
        "days": [
            {
                "date": str(a.date),
                "steps": a.steps,
                "exercise_minutes": a.exercise_minutes,
                "weight": a.weight,
                "fitness_score": a.analysis.fitness_score if a.analysis else None,
            }
            for a in activities
        ]
    }


@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from app.models.plan import FitnessPlan

    today = date.today()
    activity = (
        db.query(DailyActivity)
        .filter(DailyActivity.user_id == current_user.id, DailyActivity.date == today)
        .first()
    )
    plan = (
        db.query(FitnessPlan)
        .filter(FitnessPlan.user_id == current_user.id, FitnessPlan.date == today + timedelta(days=1))
        .first()
    )
    latest_analysis = None
    if activity and activity.analysis:
        latest_analysis = {
            "activity_level": activity.analysis.activity_level,
            "fitness_score": activity.analysis.fitness_score,
        }
    else:
        last = (
            db.query(FitnessAnalysis)
            .join(DailyActivity)
            .filter(DailyActivity.user_id == current_user.id)
            .order_by(FitnessAnalysis.created_at.desc())
            .first()
        )
        if last:
            latest_analysis = {
                "activity_level": last.activity_level,
                "fitness_score": last.fitness_score,
            }

    return {
        "user": {
            "username": current_user.username,
            "name": current_user.name,
            "weight": current_user.weight,
            "fitness_goal": current_user.fitness_goal,
            "fitness_level": current_user.fitness_level,
            "onboarding_complete": current_user.onboarding_complete,
        },
        "today": {
            "weight": activity.weight if activity else current_user.weight,
            "steps": activity.steps if activity else None,
            "exercise_minutes": activity.exercise_minutes if activity else None,
            "sleep_hours": activity.sleep_hours if activity else None,
            "water_liters": activity.water_liters if activity else None,
            "checked_in": activity is not None,
        },
        "analysis": latest_analysis,
        "tomorrow_plan": {
            "id": plan.id,
            "date": str(plan.date),
            "plan": plan.plan,
            "reason": plan.reason,
        }
        if plan
        else None,
    }
