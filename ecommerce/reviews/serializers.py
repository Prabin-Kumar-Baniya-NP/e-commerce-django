from rest_framework.serializers import ModelSerializer
from reviews.models import Reviews


class ReviewsSerializer(ModelSerializer):
    class Meta:
        model = Reviews
        fields = [
            "id",
            "user",
            "product",
            "rating",
            "comment",
            "image",
            "created_at",
            "modified_at",
        ]
        read_only_fields = [
            "created_at",
            "modified_at",
        ]


class ReviewsCreateSerializer(ModelSerializer):
    class Meta:
        model = Reviews
        fields = [
            "user",
            "product",
            "rating",
            "comment",
            "image",
        ]


class ReviewUpdateSerializer(ModelSerializer):
    class Meta:
        model = Reviews
        fields = [
            "id"
            "user",
            "product",
            "rating",
            "comment",
            "image",
        ]
        read_only_fields = ["id", "user", "product"]
