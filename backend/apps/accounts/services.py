from decimal import Decimal

from .models import UserProfile

ACTIVITY_MULTIPLIERS = {
    UserProfile.ACTIVITY_NONE: Decimal("1.2"),
    UserProfile.ACTIVITY_NORMAL: Decimal("1.375"),
    UserProfile.ACTIVITY_LIGHT: Decimal("1.55"),
    UserProfile.ACTIVITY_VERY: Decimal("1.725"),
}

GOAL_ADJUSTMENTS = {
    UserProfile.GOAL_LOSE: -500,
    UserProfile.GOAL_MAINTAIN: 0,
    UserProfile.GOAL_GAIN: 350,
}


def round_to_nearest(value, step=5):
    return int(round(float(value) / step) * step)


def calculate_bmr(profile):
    weight = Decimal(profile.current_weight or 0)
    height = Decimal(profile.height or 0)
    age = Decimal(profile.age or 0)
    base = Decimal("10") * weight + Decimal("6.25") * height - Decimal("5") * age

    if profile.gender == UserProfile.GENDER_MALE:
        return base + Decimal("5")
    if profile.gender == UserProfile.GENDER_FEMALE:
        return base - Decimal("161")
    return base - Decimal("78")


def calculate_daily_targets(profile):
    bmr = calculate_bmr(profile)
    multiplier = ACTIVITY_MULTIPLIERS.get(profile.activity_level, ACTIVITY_MULTIPLIERS[UserProfile.ACTIVITY_NORMAL])
    adjustment = GOAL_ADJUSTMENTS.get(profile.goal, 0)
    calories = max(1200, round_to_nearest(bmr * multiplier + adjustment, 25))

    weight = float(profile.current_weight or 70)
    protein_per_kg = 2 if profile.goal == UserProfile.GOAL_GAIN else 1.8 if profile.goal == UserProfile.GOAL_LOSE else 1.6
    protein = round_to_nearest(weight * protein_per_kg)
    fat = round_to_nearest((calories * 0.25) / 9)
    carbs = round_to_nearest((calories - protein * 4 - fat * 9) / 4)

    return {
        "daily_calorie_goal": calories,
        "protein_goal": max(0, protein),
        "carbs_goal": max(80, carbs),
        "fat_goal": max(0, fat),
    }


def recalculate_profile_targets(profile, save=True):
    if not profile.has_calculation_inputs():
        return profile

    targets = calculate_daily_targets(profile)
    for field, value in targets.items():
        setattr(profile, field, value)

    profile.onboarding_completed = True
    if save:
        profile.save(update_fields=[*targets.keys(), "onboarding_completed", "updated_at"])
    return profile
