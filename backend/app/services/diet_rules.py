"""Controlled food catalog for tomorrow's diet recommendations."""

from __future__ import annotations

from typing import Any


FOOD_CATALOG: list[dict[str, Any]] = [
    {"name": "Oats", "amount": "50 g", "diet": "both", "allergens": ["gluten"], "meal": "breakfast"},
    {"name": "Banana", "amount": "1 medium", "diet": "both", "allergens": [], "meal": "breakfast"},
    {"name": "Vegetable poha", "amount": "1 bowl (150 g)", "diet": "veg", "allergens": [], "meal": "breakfast"},
    {"name": "Idli", "amount": "3 pieces", "diet": "veg", "allergens": [], "meal": "breakfast"},
    {"name": "Eggs", "amount": "2", "diet": "non_veg", "allergens": ["eggs"], "meal": "breakfast"},
    {"name": "Boiled egg whites", "amount": "3", "diet": "non_veg", "allergens": ["eggs"], "meal": "breakfast"},
    {"name": "Curd", "amount": "100 g", "diet": "both", "allergens": ["dairy"], "meal": "breakfast"},
    {"name": "Steamed rice", "amount": "150 g", "diet": "both", "allergens": [], "meal": "lunch"},
    {"name": "Roti", "amount": "2", "diet": "both", "allergens": ["gluten"], "meal": "lunch"},
    {"name": "Dal", "amount": "1 bowl (150 g)", "diet": "veg", "allergens": [], "meal": "lunch"},
    {"name": "Paneer", "amount": "80 g", "diet": "veg", "allergens": ["dairy"], "meal": "lunch"},
    {"name": "Chicken", "amount": "100 g", "diet": "non_veg", "allergens": ["chicken"], "meal": "lunch"},
    {"name": "Fish", "amount": "100 g", "diet": "non_veg", "allergens": ["fish"], "meal": "lunch"},
    {"name": "Mixed vegetables", "amount": "150 g", "diet": "both", "allergens": [], "meal": "lunch"},
    {"name": "Salad", "amount": "100 g", "diet": "both", "allergens": [], "meal": "lunch"},
    {"name": "Steamed rice", "amount": "120 g", "diet": "both", "allergens": [], "meal": "dinner", "alias": "Steamed rice (dinner)"},
    {"name": "Roti", "amount": "2", "diet": "both", "allergens": ["gluten"], "meal": "dinner"},
    {"name": "Dal", "amount": "1 bowl (150 g)", "diet": "veg", "allergens": [], "meal": "dinner"},
    {"name": "Paneer", "amount": "80 g", "diet": "veg", "allergens": ["dairy"], "meal": "dinner"},
    {"name": "Chicken", "amount": "100 g", "diet": "non_veg", "allergens": ["chicken"], "meal": "dinner"},
    {"name": "Fish", "amount": "100 g", "diet": "non_veg", "allergens": ["fish"], "meal": "dinner"},
    {"name": "Mixed vegetables", "amount": "150 g", "diet": "both", "allergens": [], "meal": "dinner"},
    {"name": "Sprouts", "amount": "80 g", "diet": "veg", "allergens": [], "meal": "snack"},
    {"name": "Fruit bowl", "amount": "150 g", "diet": "both", "allergens": [], "meal": "snack"},
    {"name": "Buttermilk", "amount": "200 ml", "diet": "both", "allergens": ["dairy"], "meal": "snack"},
    {"name": "Roasted peanuts", "amount": "20 g", "diet": "veg", "allergens": ["peanuts", "nuts"], "meal": "snack"},
    {"name": "Boiled egg", "amount": "1", "diet": "non_veg", "allergens": ["eggs"], "meal": "snack"},
]

ALLERGY_ALIASES = {
    "peanut": "peanuts",
    "peanuts": "peanuts",
    "nut": "nuts",
    "nuts": "nuts",
    "tree nuts": "nuts",
    "dairy": "dairy",
    "milk": "dairy",
    "lactose": "dairy",
    "egg": "eggs",
    "eggs": "eggs",
    "gluten": "gluten",
    "wheat": "gluten",
    "soy": "soy",
    "soya": "soy",
    "fish": "fish",
    "shellfish": "shellfish",
    "chicken": "chicken",
    "paneer": "dairy",
}


def normalize_allergies(raw: list[str] | None) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for item in raw or []:
        key = " ".join(str(item).strip().lower().split())
        if not key:
            continue
        mapped = ALLERGY_ALIASES.get(key, key)
        if mapped not in seen:
            seen.add(mapped)
            out.append(mapped)
    return out


def _item_blocked(item: dict[str, Any], allergies: list[str]) -> bool:
    name = (item.get("name") or "").lower()
    tags = [a.lower() for a in (item.get("allergens") or [])]
    for allergy in allergies:
        if allergy in tags or allergy in name:
            return True
    return False


def allowed_foods(preference: str, allergies: list[str] | None) -> list[dict[str, Any]]:
    pref = (preference or "veg").lower()
    if pref not in {"veg", "non_veg"}:
        pref = "veg"
    cleaned = normalize_allergies(allergies)
    allowed = []
    for item in FOOD_CATALOG:
        diet = item["diet"]
        if pref == "veg" and diet == "non_veg":
            continue
        if _item_blocked(item, cleaned):
            continue
        allowed.append(item)
    return allowed


def _pick(pool: list[dict[str, Any]], meal: str, names: list[str]) -> list[dict[str, str]]:
    by_name = {}
    for item in pool:
        if item["meal"] != meal:
            continue
        by_name[item["name"].lower()] = item
    picked = []
    used = set()
    for name in names:
        item = by_name.get(name.lower())
        if not item:
            continue
        key = (item["name"], item["amount"], meal)
        if key in used:
            continue
        used.add(key)
        picked.append({"name": item["name"], "amount": item["amount"]})
    if not picked:
        for item in pool:
            if item["meal"] == meal and (item["name"], item["amount"], meal) not in used:
                picked.append({"name": item["name"], "amount": item["amount"]})
                used.add((item["name"], item["amount"], meal))
                if len(picked) >= 2:
                    break
    return picked


def build_diet_plan(
    preference: str,
    allergies: list[str] | None,
    goal: str | None = None,
    feeling: str | None = None,
) -> dict[str, Any]:
    pref = (preference or "veg").lower()
    if pref not in {"veg", "non_veg"}:
        pref = "veg"
    cleaned = normalize_allergies(allergies)
    pool = allowed_foods(pref, cleaned)
    goal = (goal or "general").lower()

    if pref == "non_veg":
        breakfast_names = ["Eggs", "Banana", "Oats", "Boiled egg whites", "Idli"]
        lunch_names = ["Chicken", "Steamed rice", "Salad", "Fish", "Mixed vegetables"]
        dinner_names = ["Fish", "Mixed vegetables", "Roti", "Chicken", "Dal"]
        snack_names = ["Boiled egg", "Fruit bowl", "Sprouts"]
        if goal in {"weight_loss", "cardio"}:
            lunch_names = ["Chicken", "Salad", "Mixed vegetables", "Steamed rice"]
            dinner_names = ["Fish", "Mixed vegetables", "Salad"]
        if goal in {"muscle_gain", "weight_gain"}:
            breakfast_names = ["Eggs", "Oats", "Banana"]
            lunch_names = ["Chicken", "Steamed rice", "Salad"]
            dinner_names = ["Chicken", "Roti", "Mixed vegetables"]
    else:
        breakfast_names = ["Oats", "Banana", "Vegetable poha", "Idli", "Curd"]
        lunch_names = ["Dal", "Steamed rice", "Mixed vegetables", "Salad", "Paneer", "Roti"]
        dinner_names = ["Dal", "Roti", "Mixed vegetables", "Paneer", "Steamed rice"]
        snack_names = ["Sprouts", "Fruit bowl", "Buttermilk"]
        if goal in {"muscle_gain", "weight_gain"}:
            lunch_names = ["Paneer", "Steamed rice", "Dal", "Salad"]
            dinner_names = ["Paneer", "Roti", "Mixed vegetables"]

    if feeling == "tired":
        snack_names = ["Fruit bowl", "Buttermilk", "Sprouts"]

    meals = [
        {"meal": "Breakfast", "items": _pick(pool, "breakfast", breakfast_names)[:3]},
        {"meal": "Lunch", "items": _pick(pool, "lunch", lunch_names)[:3]},
        {"meal": "Dinner", "items": _pick(pool, "dinner", dinner_names)[:3]},
        {"meal": "Snack", "items": _pick(pool, "snack", snack_names)[:2]},
    ]

    note = "Eat simple portions and drink water with meals."
    if cleaned:
        note = f"Avoid {', '.join(cleaned)}. {note}"
    if pref == "veg":
        note = "Vegetarian day. " + note
    else:
        note = "Non-veg day. " + note

    return {
        "preference": pref,
        "allergies_excluded": cleaned,
        "meals": meals,
        "notes": note,
    }


def sanitize_diet_section(
    diet: dict[str, Any] | None,
    preference: str,
    allergies: list[str] | None,
    fallback: dict[str, Any],
) -> dict[str, Any]:
    if not isinstance(diet, dict):
        return fallback
    allowed = {(i["name"].lower(), i["meal"]) for i in allowed_foods(preference, allergies)}
    meals = []
    for meal in diet.get("meals") or []:
        label = (meal or {}).get("meal")
        slot = (label or "").strip().lower()
        items = []
        for item in (meal or {}).get("items") or []:
            name = (item or {}).get("name")
            if not name:
                continue
            if (name.lower(), slot) in allowed or any(
                name.lower() == food["name"].lower() for food in allowed_foods(preference, allergies)
            ):
                amount = (item or {}).get("amount") or next(
                    (f["amount"] for f in FOOD_CATALOG if f["name"].lower() == name.lower()),
                    "",
                )
                items.append({"name": name, "amount": amount})
        if items:
            meals.append({"meal": label or slot.title(), "items": items})
    if not meals:
        return fallback
    cleaned = dict(fallback)
    cleaned["meals"] = meals
    if diet.get("notes"):
        cleaned["notes"] = diet["notes"]
    return cleaned
