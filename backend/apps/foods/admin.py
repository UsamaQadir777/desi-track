from django.contrib import admin

from .models import FoodCategory, FoodItem


class FoodItemInline(admin.TabularInline):
    model = FoodItem
    extra = 0


@admin.register(FoodCategory)
class FoodCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon")
    search_fields = ("name",)
    inlines = [FoodItemInline]


@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "serving_type", "icon", "calories", "protein", "carbs", "fat", "is_active")
    list_filter = ("category", "serving_type", "is_active")
    search_fields = ("name", "category__name")
