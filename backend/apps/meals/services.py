from decimal import Decimal, ROUND_HALF_UP

from apps.foods.models import FoodItem

from .models import MealEntry


def quantize(value):
    return Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def get_food_factor(food, amount, amount_type):
    amount = Decimal(amount)
    serving_size = Decimal(food.serving_size_grams or 100)

    if amount_type == MealEntry.AMOUNT_GRAMS:
        if food.serving_type == FoodItem.SERVING_QUANTITY:
            return amount / serving_size
        return amount / Decimal("100")

    if food.serving_type == FoodItem.SERVING_QUANTITY:
        return amount
    return (amount * serving_size) / Decimal("100")


def calculate_entry_nutrition(food, amount, amount_type):
    factor = get_food_factor(food, amount, amount_type)
    return {
        "calories": quantize(food.calories * factor),
        "protein": quantize(food.protein * factor),
        "carbs": quantize(food.carbs * factor),
        "fat": quantize(food.fat * factor),
    }


def apply_entry_nutrition(entry):
    totals = calculate_entry_nutrition(entry.food, entry.amount, entry.amount_type)
    for field, value in totals.items():
        setattr(entry, field, value)
    return entry


def summarize_entries(entries):
    totals = {"calories": Decimal("0"), "protein": Decimal("0"), "carbs": Decimal("0"), "fat": Decimal("0")}
    for entry in entries:
        totals["calories"] += entry.calories
        totals["protein"] += entry.protein
        totals["carbs"] += entry.carbs
        totals["fat"] += entry.fat
    return {key: quantize(value) for key, value in totals.items()}
