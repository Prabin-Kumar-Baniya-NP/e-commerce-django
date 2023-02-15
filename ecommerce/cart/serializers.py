from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from cart.models import Cart, CartItem


class CartItemReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"


class CartItemWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            "id",
            "cart",
            "variant",
            "campaign",
            "quantity",
            "created_at",
            "modified_at",
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=CartItem.objects.all(), fields=["cart", "variant"]
            )
        ]


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "item",
            "modified_at",
        ]
        read_only_fields = [
            "user",
            "item",
        ]
