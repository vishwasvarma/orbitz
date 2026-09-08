from datetime import date, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.models.activity import DailyActivity
from app.models.analysis import FitnessAnalysis
from app.models.plan import FitnessPlan
from app.ml.predict import predict_fitness
from app.services.agent_service import generate_plan

ACTIVITY_FIELDS = {
    "weight",
    "steps",
    "exercise_minutes",
    "exercise_intensity",
    "exercise_types",
    "sleep_hours",
    "water_liters",
    "sitting_hours",
    "feeling",
    "exercise_breakdown",
    "medical_constraints",
    "diet_preference",
    "food_allergies",
}


def _normalize_payload(payload: dict) -> dict:
    data = {key: value for key, value in payload.items() if key in ACTIVITY_FIELDS}
    breakdown = data.get("exercise_breakdown") or {}
    typed = [name for name, minutes in breakdown.items() if int(minutes or 0) > 0]
    if typed:
        data["exercise_types"] = typed
        data["exercise_minutes"] = sum(int(minutes or 0) for minutes in breakdown.values())
    elif data.get("exercise_minutes") is None:
        data["exercise_minutes"] = 0
    data["exercise_breakdown"] = breakdown
    data["medical_constraints"] = data.get("medical_constraints") or []
    data["food_allergies"] = data.get("food_allergies") or []
    pref = (data.get("diet_preference") or "veg").lower()
    data["diet_preference"] = pref if pref in {"veg", "non_veg"} else "veg"
    return data


def save_activity_and_generate_plan(
    db: Session,
    user: User,
    payload: dict,
) -> tuple[DailyActivity, FitnessAnalysis, FitnessPlan]:
    if not user.onboarding_complete:
        raise HTTPException(status_code=400, detail="Complete onboarding first")

    today = date.today()
    payload = _normalize_payload(payload)
    existing = (
        db.query(DailyActivity)
        .filter(DailyActivity.user_id == user.id, DailyActivity.date == today)
        .first()
    )
    if existing:
        # Update today's check-in only — past days stay untouched
        for key, value in payload.items():
            setattr(existing, key, value)
        activity = existing
        if activity.analysis:
            db.delete(activity.analysis)
            db.flush()
    else:
        activity = DailyActivity(user_id=user.id, date=today, **payload)
        db.add(activity)
        db.flush()

    # Update latest weight on profile
    user.weight = payload["weight"]

    ml = predict_fitness(payload)
    analysis = FitnessAnalysis(
        daily_activity_id=activity.id,
        activity_level=ml["activity_level"],
        fitness_score=ml["fitness_score"],
    )
    db.add(analysis)
    db.flush()

    # Recent history for agent context
    history = (
        db.query(DailyActivity)
        .filter(DailyActivity.user_id == user.id)
        .order_by(DailyActivity.date.desc())
        .limit(7)
        .all()
    )
    history_summary = [
        {
            "date": str(h.date),
            "steps": h.steps,
            "exercise_minutes": h.exercise_minutes,
            "exercise_breakdown": h.exercise_breakdown or {},
            "sleep_hours": h.sleep_hours,
            "weight": h.weight,
        }
        for h in history
    ]

    context = {
        "username": user.username,
        "name": user.name,
        "fitness_goal": user.fitness_goal,
        "fitness_level": user.fitness_level,
        "age": user.age,
        "gender": user.gender,
        "height": user.height,
        "weight": payload["weight"],
        "steps": payload["steps"],
        "exercise_minutes": payload["exercise_minutes"],
        "exercise_intensity": payload["exercise_intensity"],
        "exercise_types": payload.get("exercise_types") or [],
        "exercise_breakdown": payload.get("exercise_breakdown") or {},
        "medical_constraints": payload.get("medical_constraints") or [],
        "diet_preference": payload.get("diet_preference") or "veg",
        "food_allergies": payload.get("food_allergies") or [],
        "sleep_hours": payload["sleep_hours"],
        "water_liters": payload["water_liters"],
        "sitting_hours": payload.get("sitting_hours") or 0,
        "feeling": payload.get("feeling") or "normal",
        "activity_level": ml["activity_level"],
        "fitness_score": ml["fitness_score"],
        "recent_history": history_summary,
    }

    plan_dict, reason = generate_plan(context)
    tomorrow = today + timedelta(days=1)

    existing_plan = (
        db.query(FitnessPlan)
        .filter(FitnessPlan.user_id == user.id, FitnessPlan.date == tomorrow)
        .first()
    )
    if existing_plan:
        existing_plan.plan = plan_dict
        existing_plan.reason = reason
        plan = existing_plan
    else:
        plan = FitnessPlan(
            user_id=user.id,
            date=tomorrow,
            plan=plan_dict,
            reason=reason,
        )
        db.add(plan)

    db.commit()
    db.refresh(activity)
    db.refresh(analysis)
    db.refresh(plan)
    return activity, analysis, plan
