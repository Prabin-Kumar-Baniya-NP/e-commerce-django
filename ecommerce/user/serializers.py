from rest_framework import serializers
from user.models import Address, GENDER_CHOICES
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, write_only=True, validators=[validate_password]
    )
    password2 = serializers.CharField(
        max_length=128,
        write_only=True,
    )

    class Meta:
        model = User
        exclude = [
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        ]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password2": ["Password mismatch"]})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password2")
        return User.objects.create_user(**validated_data)


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        read_only_fields = [
            "email",
        ]
        exclude = [
            "password",
            "is_email_verified",
            "is_phone_number_verified",
            "last_login",
            "date_joined",
            "last_updated",
            "is_active",
            "is_staff",
            "is_superuser",
            "groups",
            "user_permissions",
        ]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            "password",
            "groups",
            "user_permissions",
            "is_active",
            "is_staff",
            "is_superuser",
        ]


class PasswordChangeSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128, write_only=True, validators=[validate_password]
    )
    password2 = serializers.CharField(
        max_length=128,
        write_only=True,
    )

    class Meta:
        model = User
        fields = ["id", "email", "password", "password2"]
        read_only_fields = ["id", "email"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Password mismatch")
        return super().validate(attrs)

    def update(self, instance, validated_data):
        validated_data.pop("password2")
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class NestedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "middle_name", "last_name"]


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["user"]

class ResetPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(
        max_length=128, write_only=True, validators=[validate_password]
    )
    password2 = serializers.CharField(
        max_length=128,
        write_only=True,
    )

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Password mismatch")
        return super().validate(attrs)

    def update(self, instance, validated_data):
        validated_data.pop("otp")
        validated_data.pop("password2")
        instance.set_password(validated_data["password"])
        instance.save()
        return instance
