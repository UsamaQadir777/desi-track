from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import MealEntry
from .serializers import MealEntrySerializer


class MealEntryViewSet(viewsets.ModelViewSet):
    serializer_class = MealEntrySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = MealEntry.objects.filter(user=self.request.user).select_related("food", "food__category")
        date = self.request.query_params.get("date")
        meal_type = self.request.query_params.get("meal_type")

        if date:
            queryset = queryset.filter(date=date)
        if meal_type:
            queryset = queryset.filter(meal_type=meal_type)
        return queryset
