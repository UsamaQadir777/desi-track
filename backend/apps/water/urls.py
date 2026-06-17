from django.urls import path

from .views import WaterIntakeView

urlpatterns = [
    path("", WaterIntakeView.as_view(), name="water-intake"),
]
