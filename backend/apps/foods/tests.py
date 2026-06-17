from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.foods.models import FoodCategory, FoodItem
from apps.foods.seed import seed_foods


User = get_user_model()


class FoodsApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="food@example.com",
            email="food@example.com",
            password="StrongPass123",
        )
        self.client.force_authenticate(user=self.user)
        seed_foods()

    def test_food_catalog_supports_search_pagination_and_category_filter(self):
        category = FoodCategory.objects.get(name="Roti / Naan")
        response = self.client.get(f"/api/foods/?search=chapati&category={category.slug}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(response.data["count"], 1)
        item = response.data["results"][0]
        self.assertEqual(item["name"], "Chapati")
        self.assertEqual(item["category_icon"], category.icon)
        self.assertEqual(item["icon"], "chapati")

    def test_food_detail_and_categories_expose_icons(self):
        item = FoodItem.objects.get(name="Samosa")
        detail = self.client.get(f"/api/foods/{item.id}/")
        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.data["serving_type"], FoodItem.SERVING_QUANTITY)

        categories = self.client.get("/api/foods/categories/")
        self.assertEqual(categories.status_code, status.HTTP_200_OK)
        self.assertTrue(any(category["icon"] for category in categories.data))
