from rest_framework import serializers
from order.models import Order
from user.serializers import AddressSerializer
from product.serializers import NestedProductSerializer, NestedVariantSerializer
from campaign.serializers import NestedCampaignSerializer


class OrderItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    product = NestedProductSerializer()
    variant = NestedVariantSerializer()
    campaign = NestedCampaignSerializer(required=False, allow_null=True)
    initial_price = serializers.FloatField()
    discount_percent = serializers.FloatField()
    final_price = serializers.FloatField()
    currency = serializers.CharField()


class OrderSerializer(serializers.ModelSerializer):
    shipping_address = AddressSerializer()
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = "__all__"
