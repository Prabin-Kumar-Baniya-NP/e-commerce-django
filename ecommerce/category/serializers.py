from rest_framework.serializers import ModelSerializer
from category.models import Category


class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class CategoryDetailSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "created_at", "modified_at"]
