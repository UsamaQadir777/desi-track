from django.conf import settings
from django.db import models


class WaterIntake(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="water_intakes")
    date = models.DateField()
    amount_ml = models.PositiveIntegerField(default=0)
    goal_ml = models.PositiveIntegerField(default=2000)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "date")
        ordering = ["-date"]
        indexes = [models.Index(fields=["user", "date"])]

    def __str__(self):
        return f"{self.user} - {self.date} - {self.amount_ml}ml"
