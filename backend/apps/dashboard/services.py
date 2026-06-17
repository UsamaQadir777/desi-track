from collections import defaultdict

from apps.accounts.models import UserProfile
from apps.meals.models import MealEntry
from apps.meals.services import summarize_entries
from apps.water.models import WaterIntake


def number(value):
    return float(value)


def serialize_entry(entry):
    return {
        "id": entry.id,
        "food": entry.food_id,
        "food_name": entry.food.name,
        "food_category": entry.food.category.name,
        "amount": number(entry.amount),
        "amount_type": entry.amount_type,
        "calories": number(entry.calories),
        "protein": number(entry.protein),
        "carbs": number(entry.carbs),
        "fat": number(entry.fat),
    }


def build_task_summary(entries, water):
    meal_types_logged = {entry.meal_type for entry in entries}
    return [
        {
            "id": "water",
            "label": "Stay hydrated",
            "done": water.amount_ml >= water.goal_ml,
        },
        {
            "id": "breakfast",
            "label": "Breakfast",
            "done": MealEntry.BREAKFAST in meal_types_logged,
        },
        {
            "id": "all_meals",
            "label": "Log at least three meals",
            "done": len(meal_types_logged) >= 3,
        },
    ]


def get_dashboard(user, date):
    profile, _ = UserProfile.objects.get_or_create(
        user=user,
        defaults={"name": user.first_name or user.email},
    )
    entries = list(
        MealEntry.objects.filter(user=user, date=date)
        .select_related("food", "food__category")
        .order_by("meal_type", "-created_at")
    )
    totals = summarize_entries(entries)
    water, _ = WaterIntake.objects.get_or_create(user=user, date=date)

    grouped_entries = defaultdict(list)
    for entry in entries:
        grouped_entries[entry.meal_type].append(entry)

    meal_summary = []
    for meal_type, meal_label in MealEntry.MEAL_TYPE_CHOICES:
        meal_entries = grouped_entries.get(meal_type, [])
        meal_totals = summarize_entries(meal_entries)
        meal_summary.append({
            "meal_type": meal_type,
            "label": meal_label,
            "totals": {key: number(value) for key, value in meal_totals.items()},
            "foods": [serialize_entry(entry) for entry in meal_entries],
        })

    consumed_calories = number(totals["calories"])
    daily_goal = profile.daily_calorie_goal

    return {
        "date": date,
        "daily_goal": {
            "calories": daily_goal,
            "protein": profile.protein_goal,
            "carbs": profile.carbs_goal,
            "fat": profile.fat_goal,
        },
        "consumed": {key: number(value) for key, value in totals.items()},
        "remaining_calories": max(0, daily_goal - consumed_calories),
        "water": {
            "amount_ml": water.amount_ml,
            "goal_ml": water.goal_ml,
            "remaining_ml": max(0, water.goal_ml - water.amount_ml),
            "progress_percent": min(100, round((water.amount_ml / water.goal_ml) * 100)) if water.goal_ml else 0,
        },
        "tasks": build_task_summary(entries, water),
        "meal_summary": meal_summary,
    }
