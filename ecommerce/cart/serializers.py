from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from cart.models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = "__all__"
        validators = [
            UniqueTogetherValidator(
                queryset=CartItem.objects.all(), fields=["cart", "variant"]
            )
        ]


class CartSerializer(serializers.ModelSerializer):
    item = CartItemSerializer(many=True)
    
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
