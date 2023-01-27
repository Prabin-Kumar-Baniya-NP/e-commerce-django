from rest_framework import serializers
from product.models import Product, ProductAttribute, ProductVariant
from category.serializers import CategoryListSerializer


class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["id", "name", "value"]


class ProductVariantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "attribute",
            "price",
            "currency",
            "image",
        ]
        depth = 1


class ProductVariantDetailSerializer(serializers.ModelSerializer):
    attribute = ProductAttributeSerializer(many=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "product",
            "attribute",
            "price",
            "currency",
            "image",
        ]


class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(many=True)
    variant = ProductVariantListSerializer(many=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "category", "variant"]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(many=True)
    variant = ProductVariantListSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "variant",
        ]
