from rest_framework import serializers
from product.models import Product, ProductAttribute, ProductVariant
from category.serializers import CategoryListSerializer
from inventory.serializers import NestedInventorySerializer
from campaign.serializers import CampaignReadSerializer


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
            "is_default",
        ]


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(many=True)
    campaign = CampaignReadSerializer(many=True)
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
            "campaign",
            "variant",
            "rating_average",
            "rating_count",
        ]


class NestedVariantSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=True)

    class Meta:
        model = ProductVariant
        fields = ["id", "attribute", "sku", "image", "is_default"]


class NestedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
        ]
