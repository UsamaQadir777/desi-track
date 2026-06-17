from django.urls import path

from .views import FoodCatalogView, FoodCategoryListView, FoodItemDetailView

urlpatterns = [
    path("categories/", FoodCategoryListView.as_view(), name="food-categories"),
    path("", FoodCatalogView.as_view(), name="food-catalog"),
    path("<int:pk>/", FoodItemDetailView.as_view(), name="food-detail"),
]
