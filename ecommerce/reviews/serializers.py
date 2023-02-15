from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Reviews
from user.serializers import NestedUserSerializer


class ReviewsReadSerializer(serializers.ModelSerializer):
    user = NestedUserSerializer()

    class Meta:
        model = Reviews
        exclude = ["is_approved"]


class ReviewsWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=Reviews.objects.all(), fields=["user", "product"]
            )
        ]


class ReviewsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = "__all__"
        read_only_fields = ["user", "product"]
