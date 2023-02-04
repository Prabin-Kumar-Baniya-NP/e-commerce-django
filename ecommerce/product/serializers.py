from rest_framework import serializers
from product.models import Product, ProductAttribute, ProductVariant
from reviews.models import Reviews
from category.serializers import CategoryListSerializer
from inventory.serializers import InventoryReadSerializer


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["id", "name", "value"]


class ProductVariantSerializer(serializers.ModelSerializer):
    inventory = InventoryReadSerializer()

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "attribute",
            "price",
            "currency",
            "inventory",
            "image",
        ]
        depth = 1


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(many=True)
    variant = ProductVariantSerializer(many=True)
    ratings = serializers.SerializerMethodField(method_name="get_ratings")

    class Meta:
        model = Product
        fields = ["id", "name", "description", "category", "ratings", "variant"]

    def get_ratings(self, obj):
        return Reviews.get_reviews_summary(obj.id)

