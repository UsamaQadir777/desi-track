from django.contrib import admin

from .models import WaterIntake


@admin.register(WaterIntake)
class WaterIntakeAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "amount_ml", "goal_ml")
    list_filter = ("date",)
    search_fields = ("user__email",)
