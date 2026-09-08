"""
Controlled exercise catalog + rule helpers for the AI agent.
The agent may only pick from this list based on level / goal / recovery.
"""

from typing import Any


EXERCISE_CATALOG: dict[str, list[dict[str, Any]]] = {
    "beginner": [
        {"name": "Walking", "category": "activity", "minutes": [15, 20, 25]},
        {"name": "Squats", "category": "strength", "sets": [2, 3], "reps": [8, 10, 12]},
        {"name": "Push-ups (knee or wall)", "category": "strength", "sets": [2, 3], "reps": [5, 8, 10]},
        {"name": "Lunges", "category": "strength", "sets": [2, 3], "reps": [8, 10]},
        {"name": "Glute bridges", "category": "strength", "sets": [2, 3], "reps": [10, 12]},
        {"name": "Stretching", "category": "recovery", "minutes": [5, 8, 10]},
        {"name": "Yoga flow (light)", "category": "recovery", "minutes": [10, 15]},
        {"name": "Marching in place", "category": "activity", "minutes": [10, 15]},
    ],
    "intermediate": [
        {"name": "Brisk walking", "category": "activity", "minutes": [20, 30]},
        {"name": "Jogging", "category": "activity", "minutes": [15, 20, 25]},
        {"name": "Cycling", "category": "activity", "minutes": [20, 30]},
        {"name": "Squats", "category": "strength", "sets": [3, 4], "reps": [10, 12, 15]},
        {"name": "Push-ups", "category": "strength", "sets": [3, 4], "reps": [8, 12, 15]},
        {"name": "Lunges", "category": "strength", "sets": [3], "reps": [10, 12]},
        {"name": "Plank", "category": "strength", "seconds": [20, 30, 45]},
        {"name": "Dumbbell rows", "category": "strength", "sets": [3], "reps": [10, 12]},
        {"name": "Stretching", "category": "recovery", "minutes": [8, 10]},
        {"name": "Yoga", "category": "recovery", "minutes": [15, 20]},
    ],
    "advanced": [
        {"name": "Running", "category": "activity", "minutes": [25, 35, 45]},
        {"name": "Interval sprints", "category": "activity", "minutes": [15, 20]},
        {"name": "Cycling", "category": "activity", "minutes": [30, 45]},
        {"name": "Barbell squats", "category": "strength", "sets": [4, 5], "reps": [6, 8, 10]},
        {"name": "Push-ups", "category": "strength", "sets": [4], "reps": [15, 20]},
        {"name": "Pull-ups / assisted", "category": "strength", "sets": [3, 4], "reps": [5, 8, 10]},
        {"name": "Deadlift (light-moderate)", "category": "strength", "sets": [3, 4], "reps": [5, 8]},
        {"name": "Plank", "category": "strength", "seconds": [45, 60, 90]},
        {"name": "Burpees", "category": "strength", "sets": [3], "reps": [8, 10]},
        {"name": "Mobility work", "category": "recovery", "minutes": [10, 15]},
        {"name": "Stretching", "category": "recovery", "minutes": [10]},
    ],
}


GOAL_FOCUS = {
    "muscle_gain": "Prioritize strength exercises with progressive sets/reps. Keep cardio light.",
    "weight_gain": "Strength focus plus adequate recovery and hydration/sleep cues for surplus.",
    "weight_loss": "Emphasize walking/cardio and moderate strength. Keep volume sustainable.",
    "cardio": "Prioritize activity/endurance pieces; keep strength supportive and short.",
    "general": "Balanced mix of activity, strength, and recovery.",
}


def intensity_for_context(level: str, feeling: str, activity_level: str) -> str:
    if feeling == "tired" or activity_level == "HIGH":
        return "light"
    if level == "beginner":
        return "low_to_moderate"
    if feeling == "energetic" and activity_level == "LOW":
        return "moderate_to_high"
    return "moderate"


def catalog_for_level(level: str) -> list[dict[str, Any]]:
    key = (level or "beginner").lower()
    return EXERCISE_CATALOG.get(key, EXERCISE_CATALOG["beginner"])


MEDICAL_CONSTRAINTS: dict[str, dict[str, Any]] = {
    "knee_pain": {
        "label": "Knee pain",
        "exclude": [
            "squat", "lunge", "running", "run", "sprint", "burpee",
            "jogging", "jog", "deadlift", "interval",
        ],
    },
    "back_pain": {
        "label": "Lower back pain",
        "exclude": ["deadlift", "barbell squat", "burpee", "sprint"],
    },
    "shoulder_pain": {
        "label": "Shoulder pain",
        "exclude": ["push-up", "push up", "pull-up", "pull up", "dumbbell row", "plank"],
    },
    "wrist_pain": {
        "label": "Wrist pain",
        "exclude": ["push-up", "push up", "plank", "burpee"],
    },
    "ankle_pain": {
        "label": "Ankle / foot pain",
        "exclude": ["running", "run", "sprint", "jogging", "jog", "burpee", "interval"],
    },
    "hip_pain": {
        "label": "Hip pain",
        "exclude": ["lunge", "squat", "deadlift", "sprint", "burpee"],
    },
    "neck_pain": {
        "label": "Neck pain",
        "exclude": ["burpee", "sprint"],
    },
    "heart_condition": {
        "label": "Heart condition",
        "exclude": ["sprint", "interval", "burpee", "running", "run"],
    },
    "asthma": {
        "label": "Asthma / breathing",
        "exclude": ["sprint", "interval", "burpee"],
    },
    "high_blood_pressure": {
        "label": "High blood pressure",
        "exclude": ["sprint", "interval", "burpee"],
    },
    "recent_surgery": {
        "label": "Recent injury / surgery",
        "exclude": [
            "squat", "lunge", "deadlift", "push-up", "push up", "pull-up",
            "burpee", "sprint", "running", "run", "jogging", "plank",
        ],
    },
    "dizziness": {
        "label": "Dizziness / lightheaded",
        "exclude": ["sprint", "interval", "burpee", "running"],
    },
}


def medical_labels(constraints: list[str] | None) -> list[str]:
    labels = []
    for key in constraints or []:
        info = MEDICAL_CONSTRAINTS.get(key)
        if info:
            labels.append(info["label"])
        elif key:
            labels.append(key.replace("_", " "))
    return labels


def _name_blocked(name: str, exclude_tokens: list[str]) -> bool:
    lowered = name.lower()
    return any(token in lowered for token in exclude_tokens)


def excluded_exercise_names(catalog: list[dict[str, Any]], constraints: list[str] | None) -> list[str]:
    tokens: list[str] = []
    for key in constraints or []:
        info = MEDICAL_CONSTRAINTS.get(key)
        if info:
            tokens.extend(info["exclude"])
    if not tokens:
        return []
    blocked = []
    for item in catalog:
        name = item.get("name") or ""
        if _name_blocked(name, tokens):
            blocked.append(name)
    return blocked


def filter_catalog_by_medical(
    catalog: list[dict[str, Any]],
    constraints: list[str] | None,
) -> tuple[list[dict[str, Any]], list[str]]:
    blocked = set(excluded_exercise_names(catalog, constraints))
    allowed = [item for item in catalog if item.get("name") not in blocked]
    return allowed, sorted(blocked)
