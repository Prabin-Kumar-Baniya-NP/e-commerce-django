from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Reviews
from user.serializers import NestedUserSerializer


class ReviewsReadSerializer(ModelSerializer):
    user = NestedUserSerializer()

    class Meta:
        model = Reviews
        fields = "__all__"


class ReviewsWriteSerializer(ModelSerializer):
    class Meta:
        model = Reviews
        fields = "__all__"
        read_only_fields = [
            "id",
            "created_at",
            "modified_at",
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Reviews.objects.all(), fields=["user", "product"]
            )
        ]


class ReviewsUpdateSerializer(ModelSerializer):
    class Meta:
        model = Reviews
        fields = "__all__"
        read_only_fields = [
            "id",
            "user",
            "product",
            "created_at",
            "modified_at",
        ]
