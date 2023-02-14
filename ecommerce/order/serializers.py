from django.db import transaction
from rest_framework import serializers
from order.models import Order, OrderItem
from cart.models import Cart, CartItem
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model
from user.serializers import AddressSerializer
from campaign.serializers import NestedCampaignSerializer
from product.serializers import NestedVariantSerializer

User = get_user_model()


class OrderItemSerializer(serializers.ModelSerializer):
    variant = NestedVariantSerializer()
    campaign = NestedCampaignSerializer()

    class Meta:
        model = OrderItem
        fields = "__all__"


class OrderReadSerializer(serializers.ModelSerializer):
    shipping_address = AddressSerializer()
    order_item = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "shipping_address",
            "total_price",
            "currency",
            "order_item",
            "created_at",
            "modified_at",
        ]


class OrderWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "shipping_address",
            "order_item",
            "created_at",
            "modified_at",
        ]
        read_only_fields = ["user", "created_at", "modified_at"]

    def create(self, validated_data):
        try:
            user = User.objects.get(id=self.context["user_id"])
            cart = Cart.objects.get(user=user)
        except User.DoesNotExist:
            raise NotFound("User not found")

        except Cart.DoesNotExist:
            raise NotFound("Cart not found")

        cart_item_list = cart.item.all()
        if not cart_item_list.exists():
            raise NotFound("Cart Item not found")

        with transaction.atomic():
            cart = user.cart
            order = Order.objects.create(
                user=user,
                status="CREATED",
                shipping_address=validated_data["shipping_address"],
                total_price=cart.get_total_cart_price(),
                currency="USD",
            )

            order_item_list = [
                OrderItem(
                    order=order,
                    variant=item.variant,
                    campaign=item.campaign,
                    quantity=item.quantity,
                    final_price=item.get_total_item_price(),
                    currency=item.variant.currency,
                )
                for item in cart_item_list
            ]
            OrderItem.objects.bulk_create(order_item_list)
            CartItem.objects.filter(cart=cart).delete()
        return order
