from django.db.models import Prefetch, Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import FoodCategory, FoodItem
from .serializers import FoodCategorySerializer, FoodItemSerializer


class FoodCatalogView(generics.ListAPIView):
    serializer_class = FoodItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search = self.request.query_params.get("search", "").strip()
        category = self.request.query_params.get("category", "").strip()
        queryset = FoodItem.objects.filter(is_active=True).select_related("category")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(category__name__icontains=search)
            )
        if category:
            if category.isdigit():
                queryset = queryset.filter(category_id=category)
            else:
                queryset = queryset.filter(Q(category__slug=category) | Q(category__name__iexact=category))
        return queryset


class FoodCategoryListView(generics.ListAPIView):
    serializer_class = FoodCategorySerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        active_items = FoodItem.objects.filter(is_active=True)
        return FoodCategory.objects.prefetch_related(Prefetch("items", queryset=active_items))


class FoodItemDetailView(generics.RetrieveAPIView):
    queryset = FoodItem.objects.filter(is_active=True).select_related("category")
    serializer_class = FoodItemSerializer
    permission_classes = [IsAuthenticated]
