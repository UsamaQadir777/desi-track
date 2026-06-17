from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.accounts.models import UserProfile


User = get_user_model()


class AccountsApiTests(APITestCase):
    def test_signup_login_refresh_logout_and_me_flow(self):
        signup_payload = {
            "name": "Ayesha Khan",
            "email": "ayesha@example.com",
            "password": "StrongPass123",
        }
        signup = self.client.post("/api/auth/signup/", signup_payload, format="json")
        self.assertEqual(signup.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", signup.data)
        self.assertIn("refresh", signup.data)
        self.assertEqual(signup.data["user"]["email"], "ayesha@example.com")

        duplicate = self.client.post("/api/auth/signup/", signup_payload, format="json")
        self.assertEqual(duplicate.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(duplicate.data["error"]["code"], "validation_error")

        login = self.client.post(
            "/api/auth/login/",
            {"email": "ayesha@example.com", "password": "StrongPass123"},
            format="json",
        )
        self.assertEqual(login.status_code, status.HTTP_200_OK)
        self.assertIn("access", login.data)

        refresh = self.client.post(
            "/api/auth/refresh/",
            {"refresh": signup.data["refresh"]},
            format="json",
        )
        self.assertEqual(refresh.status_code, status.HTTP_200_OK)
        self.assertIn("access", refresh.data)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login.data['access']}")
        me = self.client.get("/api/auth/me/")
        self.assertEqual(me.status_code, status.HTTP_200_OK)
        self.assertEqual(me.data["profile"]["name"], "Ayesha Khan")

        logout = self.client.post(
            "/api/auth/logout/",
            {"refresh": login.data["refresh"]},
            format="json",
        )
        self.assertEqual(logout.status_code, status.HTTP_204_NO_CONTENT)

    def test_profile_update_recalculates_goals_and_requires_auth(self):
        user = User.objects.create_user(
            username="ali@example.com",
            email="ali@example.com",
            password="StrongPass123",
        )
        UserProfile.objects.create(user=user, name="Ali")

        unauthenticated = self.client.get("/api/profile/")
        self.assertEqual(unauthenticated.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", unauthenticated.data)

        self.client.force_authenticate(user=user)
        incomplete = self.client.patch("/api/profile/", {"age": 30}, format="json")
        self.assertEqual(incomplete.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.patch(
            "/api/profile/",
            {
                "goal": "lose",
                "age": 30,
                "gender": "male",
                "height": "175.00",
                "current_weight": "82.00",
                "activity_level": "light_active",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["onboarding_completed"])
        self.assertGreater(response.data["daily_calorie_goal"], 0)
        self.assertGreater(response.data["protein_goal"], 0)
