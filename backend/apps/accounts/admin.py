from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "district", "goal", "daily_calorie_goal", "onboarding_completed")
    fields = (
        "user",
        "name",
        "district",
        "goal",
        "age",
        "gender",
        "height",
        "current_weight",
        "activity_level",
        "daily_calorie_goal",
        "protein_goal",
        "carbs_goal",
        "fat_goal",
        "onboarding_completed",
    )
    list_filter = ("goal", "gender", "activity_level", "onboarding_completed")
    search_fields = ("user__email", "name", "district")
