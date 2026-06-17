from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile
from .services import recalculate_profile_targets

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    RECALCULATION_FIELDS = {"goal", "age", "gender", "height", "current_weight", "activity_level"}

    class Meta:
        model = UserProfile
        fields = [
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
        ]
        read_only_fields = [
            "daily_calorie_goal",
            "protein_goal",
            "carbs_goal",
            "fat_goal",
            "onboarding_completed",
        ]

    def validate_age(self, value):
        if value is not None and not 13 <= value <= 120:
            raise serializers.ValidationError("Age must be between 13 and 120.")
        return value

    def validate_height(self, value):
        if value is not None and not 80 <= value <= 250:
            raise serializers.ValidationError("Height must be between 80cm and 250cm.")
        return value

    def validate_current_weight(self, value):
        if value is not None and not 25 <= value <= 300:
            raise serializers.ValidationError("Current weight must be between 25kg and 300kg.")
        return value

    def validate(self, attrs):
        instance = self.instance
        changing_targets = bool(self.RECALCULATION_FIELDS.intersection(attrs))
        if not changing_targets:
            return attrs

        values = {
            field: attrs.get(field, getattr(instance, field, None))
            for field in self.RECALCULATION_FIELDS
        }
        missing = [field for field, value in values.items() if value in (None, "")]
        if missing:
            raise serializers.ValidationError({
                "onboarding": f"Required before goal recalculation: {', '.join(sorted(missing))}."
            })
        return attrs

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()
        recalculate_profile_targets(instance)
        return instance


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "profile"]
        read_only_fields = ["id", "username", "email", "profile"]


class SignupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=120)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    district = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value.lower()

    def create(self, validated_data):
        email = validated_data["email"]
        user = User.objects.create_user(
            username=email,
            email=email,
            password=validated_data["password"],
            first_name=validated_data["name"],
        )
        UserProfile.objects.create(user=user, name=validated_data["name"], district=validated_data.get("district") or None)
        return user

    def to_representation(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data,
        }


class EmailTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        try:
            user = User.objects.get(email__iexact=attrs["email"])
        except User.DoesNotExist as exc:
            raise serializers.ValidationError({"email": "No account found with this email."}) from exc

        authenticated = authenticate(
            request=self.context.get("request"),
            username=user.get_username(),
            password=attrs["password"],
        )
        if authenticated is None:
            raise serializers.ValidationError({"password": "Unable to log in with the provided credentials."})
        if not authenticated.is_active:
            raise serializers.ValidationError({"email": "This account is inactive."})

        refresh = RefreshToken.for_user(authenticated)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(authenticated).data,
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self, **kwargs):
        token = RefreshToken(self.validated_data["refresh"])
        token.blacklist()
