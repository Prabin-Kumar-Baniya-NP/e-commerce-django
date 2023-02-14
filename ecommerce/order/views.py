from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from order import serializers
from order.models import Order, OrderItem
from rest_framework.exceptions import NotFound


class OrderViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post", "delete"]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.OrderReadSerializer
        return serializers.OrderWriteSerializer

    def get_object(self):
        return Order.objects.get(id=self.kwargs["pk"], user=self.request.user)

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = serializers.OrderWriteSerializer(
            data=request.data, context={"user_id": request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderItemSerializer
    http_method_names = ["get", "patch", "delete"]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return OrderItem.objects.get(id=self.kwargs["pk"])

    def get_queryset(self):
        queryset = OrderItem.objects.filter(order__user=self.request.user)
        order = self.request.query_params.get("order")
        if order:
            return queryset.filter(order__id=order)
        raise NotFound("Order id is required")
