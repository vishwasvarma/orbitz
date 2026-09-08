from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from sqlalchemy.orm import Session

from app.models.activity import DailyActivity
from app.models.analysis import FitnessAnalysis
from app.models.plan import FitnessPlan
from app.models.user import User


def _fpdf():
    from fpdf import FPDF
    from fpdf.enums import XPos, YPos

    return FPDF, XPos, YPos


def _safe(text: Any) -> str:
    return str(text or "").encode("latin-1", "replace").decode("latin-1")


def _make_pdf(title: str):
    FPDF, XPos, YPos = _fpdf()

    class OrbitzReportPdf(FPDF):
        def __init__(self, heading: str):
            super().__init__()
            self.report_title = heading
            self.set_auto_page_break(auto=True, margin=18)

        def header(self):
            self.set_font("Helvetica", "B", 16)
            self.cell(0, 10, _safe(self.report_title), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_font("Helvetica", "", 9)
            self.set_text_color(90, 90, 90)
            self.cell(0, 6, "Orbitz fitness summary  |  Not medical advice", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
            self.set_text_color(0, 0, 0)
            self.ln(2)

        def footer(self):
            self.set_y(-12)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(120, 120, 120)
            self.cell(0, 8, f"Page {self.page_no()}", align="C")

    return OrbitzReportPdf(title)


def _heading(pdf, text: str):
    from fpdf.enums import XPos, YPos

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, _safe(text), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 10)


def _line(pdf, text: str):
    from fpdf.enums import XPos, YPos

    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, _safe(text), new_x=XPos.LMARGIN, new_y=YPos.NEXT)


def _fetch_range(db: Session, user_id: int, start: date, end: date) -> list[DailyActivity]:
    return (
        db.query(DailyActivity)
        .filter(
            DailyActivity.user_id == user_id,
            DailyActivity.date >= start,
            DailyActivity.date <= end,
        )
        .order_by(DailyActivity.date.asc())
        .all()
    )


def _score(activity: DailyActivity, db: Session) -> str:
    if activity.analysis:
        return str(round(activity.analysis.fitness_score, 1))
    row = (
        db.query(FitnessAnalysis)
        .filter(FitnessAnalysis.daily_activity_id == activity.id)
        .first()
    )
    return str(round(row.fitness_score, 1)) if row else "-"


def _breakdown_text(activity: DailyActivity) -> str:
    data = activity.exercise_breakdown or {}
    if not data:
        types = ", ".join(activity.exercise_types or []) or "n/a"
        return f"{activity.exercise_minutes} min ({types})"
    parts = [f"{name} {mins} min" for name, mins in data.items()]
    return f"{activity.exercise_minutes} min total: " + ", ".join(parts)


def _plan_for(db: Session, user_id: int, day: date) -> FitnessPlan | None:
    return (
        db.query(FitnessPlan)
        .filter(FitnessPlan.user_id == user_id, FitnessPlan.date == day)
        .first()
    )


def _write_activity_block(pdf, db: Session, user: User, activity: DailyActivity):
    _heading(pdf, str(activity.date))
    _line(
        pdf,
        f"Weight {activity.weight} kg  |  Steps {activity.steps}  |  Sleep {activity.sleep_hours} h  |  "
        f"Water {activity.water_liters} L  |  Score {_score(activity, db)}",
    )
    _line(pdf, f"Exercise: {_breakdown_text(activity)}")
    if activity.medical_constraints:
        _line(pdf, "Medical constraints: " + ", ".join(activity.medical_constraints))
    if activity.diet_preference:
        allergies = ", ".join(activity.food_allergies or []) or "none"
        _line(pdf, f"Tomorrow diet: {activity.diet_preference.replace('_', '-')}  |  Allergies: {allergies}")
    plan = _plan_for(db, user.id, activity.date + timedelta(days=1))
    if plan and isinstance(plan.plan, dict):
        sections = plan.plan.get("sections") or {}
        for key in ("strength", "activity", "recovery"):
            items = sections.get(key) or []
            if not items:
                continue
            names = ", ".join(
                f"{item.get('name')} {item.get('prescription') or ''}".strip() for item in items
            )
            _line(pdf, f"Plan {key}: {names}")
        diet = sections.get("diet") or plan.plan.get("diet")
        if diet:
            meals = []
            for meal in diet.get("meals") or []:
                foods = ", ".join(
                    f"{i.get('name')} {i.get('amount') or ''}".strip() for i in (meal.get("items") or [])
                )
                meals.append(f"{meal.get('meal')}: {foods}")
            if meals:
                _line(pdf, "Diet: " + " | ".join(meals))
    pdf.ln(2)


def build_weekly_pdf(db: Session, user: User) -> bytes:
    end = date.today()
    start = end - timedelta(days=6)
    activities = _fetch_range(db, user.id, start, end)
    pdf = _make_pdf("Orbitz Weekly Report")
    pdf.add_page()
    name = user.name or user.username
    _line(pdf, f"Name: {name}")
    _line(pdf, f"Period: {start} to {end}")
    _line(pdf, f"Goal: {(user.fitness_goal or '-').replace('_', ' ')}  |  Level: {user.fitness_level or '-'}")
    pdf.ln(2)

    n = len(activities)
    _heading(pdf, "Summary")
    if not n:
        _line(pdf, "No check-ins in the last 7 days.")
        return bytes(pdf.output())

    scores = []
    for activity in activities:
        raw = _score(activity, db)
        if raw != "-":
            scores.append(float(raw))
    _line(pdf, f"Check-ins: {n}/7")
    _line(pdf, f"Avg steps: {round(sum(a.steps for a in activities) / n)}")
    _line(pdf, f"Avg exercise: {round(sum(a.exercise_minutes for a in activities) / n, 1)} min")
    _line(pdf, f"Avg sleep: {round(sum(a.sleep_hours for a in activities) / n, 1)} h")
    _line(pdf, f"Avg water: {round(sum(a.water_liters for a in activities) / n, 1)} L")
    if scores:
        _line(pdf, f"Avg fitness score: {round(sum(scores) / len(scores), 1)}")
    pdf.ln(2)

    _heading(pdf, "Daily log")
    for activity in activities:
        _write_activity_block(pdf, db, user, activity)

    return bytes(pdf.output())


def build_three_day_pdf(db: Session, user: User) -> bytes:
    end = date.today()
    start = end - timedelta(days=2)
    activities = _fetch_range(db, user.id, start, end)
    pdf = _make_pdf("Orbitz 3-Day Report")
    pdf.add_page()
    name = user.name or user.username
    _line(pdf, f"Name: {name}")
    _line(pdf, f"Period: {start} to {end}")
    pdf.ln(2)
    if not activities:
        _line(pdf, "No check-ins in the last 3 days.")
        return bytes(pdf.output())
    for activity in activities:
        _write_activity_block(pdf, db, user, activity)
    return bytes(pdf.output())
