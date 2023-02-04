from rest_framework import serializers
from product.models import Product, ProductAttribute, ProductVariant
from reviews.models import Reviews
from category.serializers import CategoryListSerializer
from inventory.serializers import NestedInventorySerializer


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["id", "name", "value"]


class NestedVariantSerializer(serializers.ModelSerializer):
    inventory = NestedInventorySerializer()
    attribute = AttributeSerializer(many=True)

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


class NestedProductSerializer(serializers.ModelSerializer):
    ratings = serializers.SerializerMethodField(method_name="get_ratings")

    class Meta:
        model = Product
        fields = ["id", "name", "description", "ratings"]

    def get_ratings(self, obj):
        return Reviews.get_reviews_summary(obj.id)


class VariantListSerializer(serializers.ModelSerializer):
    inventory = NestedInventorySerializer()
    attribute = AttributeSerializer(many=True)
    product = NestedProductSerializer()

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "product",
            "attribute",
            "price",
            "currency",
            "inventory",
            "image",
        ]
        depth = 1


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(many=True)
    variant = NestedVariantSerializer(many=True)
    ratings = serializers.SerializerMethodField(method_name="get_ratings")

    class Meta:
        model = Product
        fields = ["id", "name", "description", "category", "ratings", "variant"]

    def get_ratings(self, obj):
        return Reviews.get_reviews_summary(obj.id)
