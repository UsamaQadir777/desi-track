from django.contrib import admin

from .models import MealEntry


@admin.register(MealEntry)
class MealEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "food", "meal_type", "date", "amount", "amount_type", "calories")
    list_filter = ("meal_type", "date")
    search_fields = ("user__email", "food__name")
