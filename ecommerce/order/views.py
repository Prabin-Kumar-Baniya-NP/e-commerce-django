from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from order import serializers
from order.models import Order
from user.models import Address
from user.serializers import AddressSerializer
from cart.models import Cart, CartItem
from product.serializers import NestedProductSerializer, NestedVariantSerializer
from campaign.serializers import NestedCampaignSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer
    http_method_names = ["get", "post", "delete"]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Order.objects.get(id=self.kwargs["pk"], user=self.request.user)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            address = Address.objects.get(
                id=request.data["address_id"], user=request.user
            )
            cart = Cart.objects.get(user=request.user.id)
            cart_item_list = cart.item.all()
            if not cart_item_list.exists():
                raise CartItem.DoesNotExist

        except Address.DoesNotExist:
            raise NotFound("Address Not Found")

        except Cart.DoesNotExist:
            raise NotFound("Cart Not Found")

        except CartItem.DoesNotExist:
            raise NotFound("Cart Items Not Found")

        address_serializer = AddressSerializer(address)
        order_item_list = []
        for item in cart_item_list:
            order_item_serializer = serializers.OrderItemSerializer(
                {
                    "id": item.id,
                    "product": NestedProductSerializer(item.variant.product).data,
                    "variant": NestedVariantSerializer(item.variant).data,
                    "campaign": NestedCampaignSerializer(item.campaign).data
                    if item.campaign
                    else None,
                    "initial_price": item.variant.price,
                    "currency": item.variant.currency,
                    "discount_percent": item.campaign.discount if item.campaign else 0,
                    "final_price": item.get_item_price(),
                }
            )
            order_item_list.append(order_item_serializer.data)

        context = {
            "user": request.user.id,
            "status": "PP",
            "shipping_address": address_serializer.data,
            "order_items": order_item_list,
            "total_price": sum([item["final_price"] for item in order_item_list]),
            "currency": "USD",
        }

        serializer = serializers.OrderSerializer(data=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
