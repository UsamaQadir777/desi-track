from django.contrib import admin
from django.urls import include, path
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.views import ProfileView


class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({"status": "ok"})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", HealthCheckView.as_view(), name="health-check"),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/profile/", ProfileView.as_view(), name="profile"),
    path("api/foods/", include("apps.foods.urls")),
    path("api/meals/", include("apps.meals.urls")),
    path("api/dashboard/", include("apps.dashboard.urls")),
    path("api/progress/", include("apps.progress.urls")),
    path("api/water/", include("apps.water.urls")),
]
