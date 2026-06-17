from rest_framework import serializers

from .models import WaterIntake


class WaterIntakeSerializer(serializers.ModelSerializer):
    remaining_ml = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()

    class Meta:
        model = WaterIntake
        fields = ["id", "date", "amount_ml", "goal_ml", "remaining_ml", "progress_percent", "updated_at"]
        read_only_fields = ["id", "remaining_ml", "progress_percent", "updated_at"]

    def get_remaining_ml(self, obj):
        return max(0, obj.goal_ml - obj.amount_ml)

    def get_progress_percent(self, obj):
        if not obj.goal_ml:
            return 0
        return min(100, round((obj.amount_ml / obj.goal_ml) * 100))

    def validate_goal_ml(self, value):
        if value <= 0:
            raise serializers.ValidationError("Water goal must be greater than zero.")
        return value
