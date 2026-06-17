from datetime import date

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.foods.models import FoodCategory, FoodItem
from apps.meals.models import MealEntry
from apps.meals.services import apply_entry_nutrition


User = get_user_model()


class ProgressApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="progress@example.com",
            email="progress@example.com",
            password="StrongPass123",
        )
        self.client.force_authenticate(user=self.user)
        category = FoodCategory.objects.create(name="Progress Foods", icon="chart")
        self.food = FoodItem.objects.create(
            category=category,
            name="Progress Daal",
            calories=100,
            protein=10,
            carbs=15,
            fat=2,
        )

    def _entry(self, entry_date, amount):
        entry = MealEntry(
            user=self.user,
            food=self.food,
            meal_type=MealEntry.LUNCH,
            date=entry_date,
            amount=amount,
            amount_type=MealEntry.AMOUNT_GRAMS,
        )
        apply_entry_nutrition(entry)
        entry.save()

    def test_progress_returns_daily_totals_range_totals_and_macro_pie(self):
        self._entry(date(2026, 6, 10), 100)
        self._entry(date(2026, 6, 11), 200)

        response = self.client.get("/api/progress/?start=2026-06-10&end=2026-06-11")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["daily"]), 2)
        self.assertEqual(response.data["totals"]["calories"], 300.0)
        self.assertEqual(response.data["totals"]["protein"], 30.0)
        self.assertEqual(len(response.data["pie_chart"]), 3)
        self.assertGreater(sum(item["percent"] for item in response.data["pie_chart"]), 99)

    def test_progress_validates_date_range(self):
        response = self.client.get("/api/progress/?start=2026-06-12&end=2026-06-11")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
