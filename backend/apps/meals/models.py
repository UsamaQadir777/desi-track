from django.conf import settings
from django.db import models

from apps.foods.models import FoodItem


class MealEntry(models.Model):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    SNACKS = "snacks"
    DINNER = "dinner"
    MEAL_TYPE_CHOICES = [
        (BREAKFAST, "Breakfast"),
        (LUNCH, "Lunch"),
        (SNACKS, "Snacks"),
        (DINNER, "Dinner"),
    ]

    AMOUNT_GRAMS = "grams"
    AMOUNT_QUANTITY = "quantity"
    AMOUNT_TYPE_CHOICES = [
        (AMOUNT_GRAMS, "Grams"),
        (AMOUNT_QUANTITY, "Quantity"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="meal_entries")
    food = models.ForeignKey(FoodItem, on_delete=models.PROTECT, related_name="meal_entries")
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE_CHOICES)
    date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    amount_type = models.CharField(max_length=20, choices=AMOUNT_TYPE_CHOICES, default=AMOUNT_GRAMS)
    calories = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    protein = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    carbs = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "meal_type", "-created_at"]
        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["user", "meal_type", "date"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.food.name} - {self.date}"
