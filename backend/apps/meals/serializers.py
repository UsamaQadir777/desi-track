from rest_framework import serializers

from apps.foods.models import FoodItem

from .models import MealEntry
from .services import apply_entry_nutrition


class MealEntrySerializer(serializers.ModelSerializer):
    food_name = serializers.CharField(source="food.name", read_only=True)
    food_category = serializers.CharField(source="food.category.name", read_only=True)
    food = serializers.PrimaryKeyRelatedField(queryset=FoodItem.objects.filter(is_active=True))

    class Meta:
        model = MealEntry
        fields = [
            "id",
            "food",
            "food_name",
            "food_category",
            "meal_type",
            "date",
            "amount",
            "amount_type",
            "calories",
            "protein",
            "carbs",
            "fat",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "food_name", "food_category", "calories", "protein", "carbs", "fat", "created_at", "updated_at"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def create(self, validated_data):
        entry = MealEntry(user=self.context["request"].user, **validated_data)
        apply_entry_nutrition(entry)
        entry.save()
        return entry

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        apply_entry_nutrition(instance)
        instance.save()
        return instance
