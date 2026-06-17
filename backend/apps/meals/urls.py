from rest_framework.routers import DefaultRouter

from .views import MealEntryViewSet

router = DefaultRouter()
router.register("", MealEntryViewSet, basename="meal-entry")

urlpatterns = router.urls
