from sqlalchemy import text

from app.database.connection import Base, engine
from app.models import user, activity, analysis, plan  # noqa: F401

# Additive SQLite columns only — never drop tables or existing rows.
_ACTIVITY_COLUMNS = {
    "exercise_breakdown": "TEXT",
    "medical_constraints": "TEXT",
    "diet_preference": "VARCHAR(32)",
    "food_allergies": "TEXT",
}


def _existing_columns(table: str) -> set[str]:
    with engine.connect() as conn:
        rows = conn.execute(text(f"PRAGMA table_info({table})")).fetchall()
    return {row[1] for row in rows}


def ensure_columns() -> None:
    """Add new columns to existing SQLite tables without wiping data."""
    if "daily_activity" not in Base.metadata.tables:
        return
    try:
        existing = _existing_columns("daily_activity")
    except Exception:
        return
    if not existing:
        return
    with engine.begin() as conn:
        for name, decl in _ACTIVITY_COLUMNS.items():
            if name not in existing:
                conn.execute(text(f"ALTER TABLE daily_activity ADD COLUMN {name} {decl}"))


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    ensure_columns()
