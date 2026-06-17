from datetime import date

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import UserProfile
from apps.foods.models import FoodCategory, FoodItem
from apps.meals.models import MealEntry
from apps.meals.services import apply_entry_nutrition
from apps.water.models import WaterIntake


User = get_user_model()


class DashboardApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="dash@example.com",
            email="dash@example.com",
            password="StrongPass123",
        )
        UserProfile.objects.create(
            user=self.user,
            name="Dashboard User",
            daily_calorie_goal=2000,
            protein_goal=120,
            carbs_goal=220,
            fat_goal=65,
        )
        self.client.force_authenticate(user=self.user)
        category = FoodCategory.objects.create(name="Dashboard Foods", icon="plate")
        self.food = FoodItem.objects.create(
            category=category,
            name="Dashboard Daal",
            calories=100,
            protein=10,
            carbs=15,
            fat=2,
        )

    def _entry(self, meal_type, amount):
        entry = MealEntry(
            user=self.user,
            food=self.food,
            meal_type=meal_type,
            date=date(2026, 6, 11),
            amount=amount,
            amount_type=MealEntry.AMOUNT_GRAMS,
        )
        apply_entry_nutrition(entry)
        entry.save()
        return entry

    def test_dashboard_aggregates_totals_water_meals_and_tasks(self):
        self._entry(MealEntry.BREAKFAST, 100)
        self._entry(MealEntry.LUNCH, 100)
        self._entry(MealEntry.DINNER, 100)
        WaterIntake.objects.create(user=self.user, date=date(2026, 6, 11), amount_ml=2000, goal_ml=2000)

        response = self.client.get("/api/dashboard/?date=2026-06-11")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["consumed"]["calories"], 300.0)
        self.assertEqual(response.data["remaining_calories"], 1700.0)
        self.assertEqual(response.data["water"]["progress_percent"], 100)
        self.assertTrue(all(task["done"] for task in response.data["tasks"]))
        self.assertEqual(len(response.data["meal_summary"]), 4)
