from collections import defaultdict
from datetime import timedelta

from django.utils import timezone

from apps.meals.models import MealEntry
from apps.meals.services import summarize_entries


def number(value):
    return float(value)


def date_range(start_date, end_date):
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=1)


def get_progress(user, start_date=None, end_date=None):
    end_date = end_date or timezone.localdate()
    start_date = start_date or (end_date - timedelta(days=6))

    entries = list(
        MealEntry.objects.filter(user=user, date__range=[start_date, end_date])
        .select_related("food", "food__category")
        .order_by("date")
    )

    entries_by_date = defaultdict(list)
    for entry in entries:
        entries_by_date[entry.date].append(entry)

    daily = []
    for day in date_range(start_date, end_date):
        totals = summarize_entries(entries_by_date.get(day, []))
        daily.append({
            "date": day,
            "calories": number(totals["calories"]),
            "protein": number(totals["protein"]),
            "carbs": number(totals["carbs"]),
            "fat": number(totals["fat"]),
        })

    range_totals = {
        "calories": sum(item["calories"] for item in daily),
        "protein": sum(item["protein"] for item in daily),
        "carbs": sum(item["carbs"] for item in daily),
        "fat": sum(item["fat"] for item in daily),
    }
    macro_calories = {
        "protein": range_totals["protein"] * 4,
        "carbs": range_totals["carbs"] * 4,
        "fat": range_totals["fat"] * 9,
    }
    macro_total = sum(macro_calories.values())

    pie_chart = [
        {
            "macro": macro,
            "grams": round(range_totals[macro], 2),
            "calories": round(calories, 2),
            "percent": round((calories / macro_total) * 100, 1) if macro_total else 0,
        }
        for macro, calories in macro_calories.items()
    ]

    return {
        "range": {"start": start_date, "end": end_date},
        "daily": daily,
        "weekly_progress": daily[-7:],
        "totals": {key: round(value, 2) for key, value in range_totals.items()},
        "pie_chart": pie_chart,
    }
