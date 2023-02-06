from rest_framework import serializers
from product.models import Product, ProductAttribute, ProductVariant
from category.serializers import CategoryListSerializer
from inventory.serializers import NestedInventorySerializer


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["id", "name", "value"]


class VariantSerializer(serializers.ModelSerializer):
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


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(many=True)
    variant = VariantSerializer(many=True)
    rating_average = serializers.DecimalField(max_digits=3, decimal_places=2)
    rating_count = serializers.IntegerField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "variant",
            "rating_average",
            "rating_count",
        ]
