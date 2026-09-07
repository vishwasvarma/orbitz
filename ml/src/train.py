"""
Train Orbitz activity-level model.

Uses scikit-learn RandomForest when available.
Falls back to a pure-Python weighted ensemble (no compiler needed).
"""

from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]  # ml/
PROJECT = ROOT.parent  # orbitz/
DATA_PATH = ROOT / "data" / "fitness_data.csv"
MODEL_OUT = PROJECT / "backend" / "app" / "ml" / "model.pkl"
ML_MODEL_OUT = ROOT / "models" / "fitness_model.pkl"
META_OUT = PROJECT / "backend" / "app" / "ml" / "model_meta.json"


def synthesize_dataset(n: int = 800, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for _ in range(n):
        steps = int(rng.integers(500, 16000))
        exercise = int(rng.integers(0, 90))
        sleep = float(rng.uniform(4, 9.5))
        water = float(rng.uniform(0.5, 4.0))
        sitting = float(rng.uniform(2, 12))
        intensity = int(rng.integers(0, 3))
        feeling = int(rng.integers(0, 3))

        score = (
            min(steps / 10000, 1.2) * 35
            + min(exercise / 45, 1.2) * 30
            + intensity * 5
            + min(sleep / 8, 1.1) * 20
            + min(water / 2.5, 1.1) * 10
            - min(sitting / 10, 1.0) * 8
            + feeling * 3
            + float(rng.normal(0, 4))
        )
        if score < 45:
            label = 0
        elif score < 70:
            label = 1
        else:
            label = 2

        rows.append(
            {
                "steps": steps,
                "exercise_minutes": exercise,
                "sleep_hours": round(sleep, 1),
                "water_liters": round(water, 1),
                "sitting_hours": round(sitting, 1),
                "intensity_code": intensity,
                "feeling_code": feeling,
                "activity_level": label,
            }
        )
    return pd.DataFrame(rows)


class OrbitzEnsembleClassifier:
    """Lightweight ensemble of threshold stumps — trainable, deterministic."""

    def __init__(self, n_stumps: int = 80, seed: int = 42):
        self.n_stumps = n_stumps
        self.seed = seed
        self.stumps: list[dict] = []
        self.feature_means: list[float] = []
        self.feature_stds: list[float] = []
        self.classes_ = np.array([0, 1, 2])

    def _scale(self, X: np.ndarray) -> np.ndarray:
        return (X - self.feature_means) / self.feature_stds

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.feature_means = X.mean(axis=0)
        self.feature_stds = X.std(axis=0) + 1e-6
        Xs = self._scale(X)
        rng = np.random.default_rng(self.seed)
        self.stumps = []
        n_features = Xs.shape[1]
        for _ in range(self.n_stumps):
            feat = int(rng.integers(0, n_features))
            threshold = float(np.median(Xs[:, feat]) + rng.normal(0, 0.15))
            votes = {0: 0.0, 1: 0.0, 2: 0.0}
            left = y[Xs[:, feat] <= threshold]
            right = y[Xs[:, feat] > threshold]
            for subset, side in ((left, "left"), (right, "right")):
                if len(subset) == 0:
                    continue
                for cls in (0, 1, 2):
                    share = float(np.mean(subset == cls))
                    votes[cls] += share
            majority_left = int(np.bincount(left, minlength=3).argmax()) if len(left) else 1
            majority_right = int(np.bincount(right, minlength=3).argmax()) if len(right) else 1
            self.stumps.append(
                {
                    "feat": feat,
                    "threshold": threshold,
                    "left": majority_left,
                    "right": majority_right,
                }
            )
        return self

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        Xs = self._scale(X)
        probs = []
        for row in Xs:
            counts = np.zeros(3, dtype=float)
            for stump in self.stumps:
                pred = stump["left"] if row[stump["feat"]] <= stump["threshold"] else stump["right"]
                counts[pred] += 1
            counts = counts / counts.sum()
            probs.append(counts)
        return np.array(probs)

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.predict_proba(X).argmax(axis=1)


def train_sklearn(X_train, y_train, X_test, y_test):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import classification_report

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)
    model = RandomForestClassifier(
        n_estimators=120,
        max_depth=8,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(X_train_s, y_train)
    preds = model.predict(X_test_s)
    print(classification_report(y_test, preds, target_names=["LOW", "MODERATE", "HIGH"]))
    return {"model": model, "scaler": scaler, "backend": "sklearn"}


def train_fallback(X_train, y_train, X_test, y_test):
    model = OrbitzEnsembleClassifier()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = float(np.mean(preds == y_test))
    print(f"Fallback ensemble accuracy: {acc:.3f}")
    return {"model": model, "scaler": None, "backend": "orbitz_ensemble"}


def main() -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    (ROOT / "models").mkdir(parents=True, exist_ok=True)
    MODEL_OUT.parent.mkdir(parents=True, exist_ok=True)

    df = synthesize_dataset()
    df.to_csv(DATA_PATH, index=False)

    feature_cols = [
        "steps",
        "exercise_minutes",
        "sleep_hours",
        "water_liters",
        "sitting_hours",
        "intensity_code",
        "feeling_code",
    ]
    X = df[feature_cols].values.astype(float)
    y = df["activity_level"].values.astype(int)

    rng = np.random.default_rng(42)
    idx = rng.permutation(len(X))
    split = int(len(X) * 0.8)
    train_idx, test_idx = idx[:split], idx[split:]
    X_train, y_train = X[train_idx], y[train_idx]
    X_test, y_test = X[test_idx], y[test_idx]

    try:
        bundle = train_sklearn(X_train, y_train, X_test, y_test)
    except Exception as exc:  # noqa: BLE001
        print(f"sklearn unavailable ({exc}); using Orbitz ensemble")
        bundle = train_fallback(X_train, y_train, X_test, y_test)

    bundle["features"] = feature_cols
    joblib.dump(bundle, MODEL_OUT)
    joblib.dump(bundle, ML_MODEL_OUT)
    META_OUT.write_text(json.dumps({"backend": bundle["backend"], "features": feature_cols}, indent=2))
    print(f"Saved model -> {MODEL_OUT}")
    print(f"Saved model -> {ML_MODEL_OUT}")


if __name__ == "__main__":
    main()
