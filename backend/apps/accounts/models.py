from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    GOAL_LOSE = "lose"
    GOAL_GAIN = "gain"
    GOAL_MAINTAIN = "maintain"
    GOAL_CHOICES = [
        (GOAL_LOSE, "Lose Weight"),
        (GOAL_GAIN, "Gain Weight"),
        (GOAL_MAINTAIN, "Maintain Weight"),
    ]

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"
    GENDER_CHOICES = [
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    ]

    ACTIVITY_NONE = "no_activity"
    ACTIVITY_NORMAL = "normal_walk"
    ACTIVITY_LIGHT = "light_active"
    ACTIVITY_VERY = "very_active"
    ACTIVITY_CHOICES = [
        (ACTIVITY_NONE, "No Activity"),
        (ACTIVITY_NORMAL, "Normal Walk"),
        (ACTIVITY_LIGHT, "Gym / Light Active"),
        (ACTIVITY_VERY, "Very Active"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    name = models.CharField(max_length=120, blank=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES, default=GOAL_MAINTAIN)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default=GENDER_OTHER)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Centimeters")
    current_weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Kilograms")
    activity_level = models.CharField(max_length=30, choices=ACTIVITY_CHOICES, default=ACTIVITY_NORMAL)
    daily_calorie_goal = models.PositiveIntegerField(default=0)
    protein_goal = models.PositiveIntegerField(default=0)
    carbs_goal = models.PositiveIntegerField(default=0)
    fat_goal = models.PositiveIntegerField(default=0)
    onboarding_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["user__id"]

    def __str__(self):
        return self.name or self.user.get_username()

    def has_calculation_inputs(self):
        return all([self.age, self.height, self.current_weight, self.gender, self.goal, self.activity_level])
