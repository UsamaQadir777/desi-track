from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class WaterApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="water@example.com",
            email="water@example.com",
            password="StrongPass123",
        )
        self.client.force_authenticate(user=self.user)

    def test_water_create_update_range_and_progress(self):
        create = self.client.post(
            "/api/water/",
            {"date": "2026-06-11", "amount_ml": 750, "goal_ml": 2000},
            format="json",
        )
        self.assertEqual(create.status_code, status.HTTP_200_OK)
        self.assertEqual(create.data["remaining_ml"], 1250)
        self.assertEqual(create.data["progress_percent"], 38)

        patch = self.client.patch(
            "/api/water/",
            {"date": "2026-06-11", "amount_ml": 2000},
            format="json",
        )
        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.assertEqual(patch.data["progress_percent"], 100)

        range_response = self.client.get("/api/water/?start=2026-06-10&end=2026-06-11")
        self.assertEqual(range_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(range_response.data), 1)

    def test_water_validates_goal_and_bad_dates(self):
        invalid_goal = self.client.post(
            "/api/water/",
            {"date": "2026-06-11", "goal_ml": 0},
            format="json",
        )
        self.assertEqual(invalid_goal.status_code, status.HTTP_400_BAD_REQUEST)

        invalid_date = self.client.get("/api/water/?date=11-06-2026")
        self.assertEqual(invalid_date.status_code, status.HTTP_400_BAD_REQUEST)
