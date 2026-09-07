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
