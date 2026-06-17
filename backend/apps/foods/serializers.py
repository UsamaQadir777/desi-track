from rest_framework import serializers

from .models import FoodCategory, FoodItem


class FoodItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    category_icon = serializers.CharField(source="category.icon", read_only=True)

    class Meta:
        model = FoodItem
        fields = [
            "id",
            "category",
            "category_name",
            "category_icon",
            "name",
            "slug",
            "icon",
            "serving_type",
            "quantity_label",
            "serving_size_grams",
            "calories",
            "protein",
            "carbs",
            "fat",
        ]
        read_only_fields = ["id", "slug", "category_name"]


class FoodCategorySerializer(serializers.ModelSerializer):
    items = FoodItemSerializer(many=True, read_only=True)

    class Meta:
        model = FoodCategory
        fields = ["id", "name", "slug", "icon", "items"]
        read_only_fields = ["id", "slug"]
