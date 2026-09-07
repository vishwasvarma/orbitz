"""ML inference for activity level + fitness score."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import numpy as np

MODEL_DIR = Path(__file__).resolve().parent
MODEL_PATH = MODEL_DIR / "model.pkl"

_LEVELS = ["LOW", "MODERATE", "HIGH"]


def _feature_vector(
    steps: int,
    exercise_minutes: int,
    sleep_hours: float,
    water_liters: float,
    sitting_hours: float,
    intensity_code: int,
    feeling_code: int,
) -> np.ndarray:
    return np.array(
        [[
            steps,
            exercise_minutes,
            sleep_hours,
            water_liters,
            sitting_hours,
            intensity_code,
            feeling_code,
        ]],
        dtype=float,
    )


def _encode_intensity(value: str) -> int:
    return {"light": 0, "moderate": 1, "high": 2}.get((value or "").lower(), 1)


def _encode_feeling(value: str) -> int:
    return {"tired": 0, "normal": 1, "energetic": 2}.get((value or "").lower(), 1)


def _heuristic_predict(features: dict[str, Any]) -> tuple[str, float]:
    steps = features["steps"]
    exercise = features["exercise_minutes"]
    sleep = features["sleep_hours"]
    water = features["water_liters"]
    sitting = features["sitting_hours"]
    intensity = _encode_intensity(features.get("exercise_intensity", "moderate"))
    feeling = _encode_feeling(features.get("feeling", "normal"))

    activity_points = (
        min(steps / 10000, 1.2) * 35
        + min(exercise / 45, 1.2) * 30
        + intensity * 5
    )
    recovery_points = (
        min(sleep / 8, 1.1) * 20
        + min(water / 2.5, 1.1) * 10
        - min(sitting / 10, 1.0) * 8
        + feeling * 3
    )
    score = max(0, min(100, round(activity_points + recovery_points, 1)))

    if score < 45:
        level = "LOW"
    elif score < 70:
        level = "MODERATE"
    else:
        level = "HIGH"
    return level, float(score)


def predict_fitness(features: dict[str, Any]) -> dict[str, Any]:
    vector = _feature_vector(
        steps=int(features.get("steps", 0)),
        exercise_minutes=int(features.get("exercise_minutes", 0)),
        sleep_hours=float(features.get("sleep_hours", 0)),
        water_liters=float(features.get("water_liters", 0)),
        sitting_hours=float(features.get("sitting_hours", 0)),
        intensity_code=_encode_intensity(features.get("exercise_intensity", "moderate")),
        feeling_code=_encode_feeling(features.get("feeling", "normal")),
    )

    if not MODEL_PATH.exists():
        level, score = _heuristic_predict(features)
        return {"activity_level": level, "fitness_score": score, "source": "heuristic"}

    bundle = joblib.load(MODEL_PATH)
    model = bundle["model"]
    scaler = bundle.get("scaler")
    X = scaler.transform(vector) if scaler is not None else vector
    pred = int(model.predict(X)[0])
    level = _LEVELS[pred] if 0 <= pred < len(_LEVELS) else "MODERATE"

    proba_fn = getattr(model, "predict_proba", None)
    if proba_fn is not None:
        proba = proba_fn(X)
        conf = float(np.max(proba[0]))
        base = {"LOW": 40, "MODERATE": 65, "HIGH": 85}[level]
        score = round(base * 0.7 + conf * 30 + min(features.get("sleep_hours", 0) / 8, 1) * 5, 1)
    else:
        _, score = _heuristic_predict(features)

    score = float(max(0, min(100, score)))
    return {
        "activity_level": level,
        "fitness_score": score,
        "source": bundle.get("backend", "model"),
    }
