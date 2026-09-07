from __future__ import annotations

import json
import re
from typing import Any

from groq import Groq

from app.config import get_settings
from app.services.exercise_rules import (
    GOAL_FOCUS,
    catalog_for_level,
    intensity_for_context,
)


def _rule_based_plan(context: dict[str, Any]) -> dict[str, Any]:
    """Deterministic fallback if Groq is unavailable."""
    level = (context.get("fitness_level") or "beginner").lower()
    goal = context.get("fitness_goal") or "general"
    feeling = context.get("feeling") or "normal"
    activity_level = context.get("activity_level") or "MODERATE"
    catalog = catalog_for_level(level)
    intensity = intensity_for_context(level, feeling, activity_level)

    strength = [e for e in catalog if e["category"] == "strength"]
    activity = [e for e in catalog if e["category"] == "activity"]
    recovery = [e for e in catalog if e["category"] == "recovery"]

    # Tired / high previous load → lighter plan
    if feeling == "tired" or activity_level == "HIGH":
        pick_strength = strength[:2]
        pick_activity = activity[:1]
        pick_recovery = recovery[:2]
        walk_note = "Keep it easy — recovery priority"
    else:
        pick_strength = strength[:3]
        pick_activity = activity[:1]
        pick_recovery = recovery[:1]
        walk_note = "Steady pace"

    def format_ex(e: dict) -> dict:
        item = {"name": e["name"], "category": e["category"]}
        if "sets" in e and "reps" in e:
            item["sets"] = e["sets"][0]
            item["reps"] = e["reps"][min(1, len(e["reps"]) - 1)]
            item["prescription"] = f"{item['sets']} x {item['reps']}"
        elif "seconds" in e:
            item["seconds"] = e["seconds"][0]
            item["prescription"] = f"{item['seconds']} sec"
        elif "minutes" in e:
            mins = e["minutes"][0] if feeling == "tired" else e["minutes"][min(1, len(e["minutes"]) - 1)]
            item["minutes"] = mins
            item["prescription"] = f"{mins} min"
        return item

    strength_items = [format_ex(e) for e in pick_strength]
    activity_items = [format_ex(e) for e in pick_activity]
    recovery_items = [format_ex(e) for e in pick_recovery]

    # Goal tweak
    if goal == "cardio" and activity:
        activity_items = [format_ex(activity[0])]
        if len(activity) > 1:
            activity_items.append(format_ex(activity[1]))
    if goal in ("muscle_gain", "weight_gain") and len(strength) >= 3:
        strength_items = [format_ex(e) for e in strength[:3]]

    water_target = "2-2.5 L" if float(context.get("water_liters") or 0) < 2 else "2.5-3 L"
    sleep_target = "7-8 hours"

    return {
        "title": "Tomorrow's Plan",
        "intensity": intensity,
        "sections": {
            "strength": strength_items,
            "activity": activity_items,
            "recovery": recovery_items,
            "hydration": {"aim": water_target},
            "sleep": {"aim": sleep_target},
        },
        "notes": walk_note,
        "goal_focus": GOAL_FOCUS.get(goal, GOAL_FOCUS["general"]),
    }


def _extract_json(text: str) -> dict[str, Any] | None:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
    return None


def generate_plan(context: dict[str, Any]) -> tuple[dict[str, Any], str]:
    """
    Returns (plan_dict, reason).
    Uses Groq LLM constrained to the exercise catalog; falls back to rules.
    """
    settings = get_settings()
    level = (context.get("fitness_level") or "beginner").lower()
    goal = context.get("fitness_goal") or "general"
    catalog = catalog_for_level(level)
    intensity = intensity_for_context(
        level,
        context.get("feeling") or "normal",
        context.get("activity_level") or "MODERATE",
    )
    fallback = _rule_based_plan(context)
    reason = (
        f"Based on {goal.replace('_', ' ')} goal, {level} level, "
        f"ML activity={context.get('activity_level')}, feeling={context.get('feeling')}."
    )

    if not settings.groq_api_key:
        fallback["source"] = "rules"
        return fallback, reason + " (rule-based; no Groq key)"

    allowed_names = [e["name"] for e in catalog]
    system = (
        "You are Orbitz, a fitness planning agent. "
        "You MUST only choose exercises from the provided catalog. "
        "Never invent new exercise names. "
        "Respect fitness level, recovery, and daily limits. "
        "Return ONLY valid JSON matching the schema."
    )
    user_prompt = f"""
Create tomorrow's personalized fitness plan.

User context:
{json.dumps(context, indent=2)}

Goal focus: {GOAL_FOCUS.get(goal, GOAL_FOCUS['general'])}
Target intensity: {intensity}

ALLOWED EXERCISE CATALOG (choose only from these):
{json.dumps(catalog, indent=2)}

Allowed exercise names exactly:
{allowed_names}

Return JSON with this shape:
{{
  "title": "Tomorrow's Plan",
  "intensity": "{intensity}",
  "sections": {{
    "strength": [{{"name": "...", "prescription": "3 × 10"}}],
    "activity": [{{"name": "...", "prescription": "20 min"}}],
    "recovery": [{{"name": "...", "prescription": "5 min"}}],
    "hydration": {{"aim": "2–2.5 L"}},
    "sleep": {{"aim": "7–8 hours"}}
  }},
  "notes": "short coaching note",
  "goal_focus": "one sentence"
}}

Rules:
- If feeling is tired OR activity_level is HIGH → lighter plan, more recovery.
- Beginner → low/moderate only.
- Prefer 2–4 strength items, 1 activity, 1 recovery.
- Every exercise name MUST be in the allowed list.
"""

    try:
        client = Groq(api_key=settings.groq_api_key)
        completion = client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.4,
            max_tokens=1200,
        )
        content = completion.choices[0].message.content or ""
        parsed = _extract_json(content)
        if not parsed:
            fallback["source"] = "rules_fallback"
            return fallback, reason + " (Groq parse fallback)"

        # Validate exercise names against catalog
        allowed = set(allowed_names)
        for key in ("strength", "activity", "recovery"):
            items = parsed.get("sections", {}).get(key, [])
            if not isinstance(items, list):
                continue
            cleaned = []
            for item in items:
                name = (item or {}).get("name")
                if name in allowed:
                    cleaned.append(item)
            parsed.setdefault("sections", {})[key] = cleaned

        # Ensure hydration/sleep exist
        sections = parsed.setdefault("sections", {})
        sections.setdefault("hydration", fallback["sections"]["hydration"])
        sections.setdefault("sleep", fallback["sections"]["sleep"])
        if not sections.get("strength") and not sections.get("activity"):
            fallback["source"] = "rules_fallback"
            return fallback, reason + " (empty plan fallback)"

        parsed["source"] = "groq+rules"
        parsed.setdefault("intensity", intensity)
        return parsed, reason + " (Groq agent + controlled catalog)"
    except Exception as exc:  # noqa: BLE001
        fallback["source"] = "rules_fallback"
        return fallback, reason + f" (Groq error: {exc})"
