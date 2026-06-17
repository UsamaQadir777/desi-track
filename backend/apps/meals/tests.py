from datetime import date

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.foods.models import FoodCategory, FoodItem
from apps.meals.models import MealEntry


User = get_user_model()


class MealsApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="meal@example.com",
            email="meal@example.com",
            password="StrongPass123",
        )
        self.other_user = User.objects.create_user(
            username="other@example.com",
            email="other@example.com",
            password="StrongPass123",
        )
        self.client.force_authenticate(user=self.user)
        self.category = FoodCategory.objects.create(name="Test Roti", icon="bread")
        self.grams_food = FoodItem.objects.create(
            category=self.category,
            name="Test Daal",
            calories=100,
            protein=10,
            carbs=15,
            fat=2,
        )
        self.quantity_food = FoodItem.objects.create(
            category=self.category,
            name="Test Chapati",
            serving_type=FoodItem.SERVING_QUANTITY,
            quantity_label="1 roti",
            serving_size_grams=50,
            calories=120,
            protein=4,
            carbs=22,
            fat=2,
        )

    def test_meal_crud_scopes_to_user_and_calculates_grams(self):
        response = self.client.post(
            "/api/meals/",
            {
                "food": self.grams_food.id,
                "meal_type": MealEntry.LUNCH,
                "date": "2026-06-11",
                "amount": "150.00",
                "amount_type": MealEntry.AMOUNT_GRAMS,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["calories"], "150.00")
        self.assertEqual(response.data["protein"], "15.00")

        MealEntry.objects.create(
            user=self.other_user,
            food=self.grams_food,
            meal_type=MealEntry.DINNER,
            date=date(2026, 6, 11),
            amount=100,
            amount_type=MealEntry.AMOUNT_GRAMS,
            calories=100,
        )
        list_response = self.client.get("/api/meals/?date=2026-06-11")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.data["count"], 1)

        entry_id = response.data["id"]
        patch = self.client.patch(f"/api/meals/{entry_id}/", {"amount": "200.00"}, format="json")
        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.assertEqual(patch.data["calories"], "200.00")

        delete = self.client.delete(f"/api/meals/{entry_id}/")
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_quantity_food_calculation_and_amount_validation(self):
        response = self.client.post(
            "/api/meals/",
            {
                "food": self.quantity_food.id,
                "meal_type": MealEntry.BREAKFAST,
                "date": "2026-06-11",
                "amount": "2.00",
                "amount_type": MealEntry.AMOUNT_QUANTITY,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["calories"], "240.00")

        invalid = self.client.post(
            "/api/meals/",
            {
                "food": self.quantity_food.id,
                "meal_type": MealEntry.BREAKFAST,
                "date": "2026-06-11",
                "amount": "0.00",
                "amount_type": MealEntry.AMOUNT_QUANTITY,
            },
            format="json",
        )
        self.assertEqual(invalid.status_code, status.HTTP_400_BAD_REQUEST)
