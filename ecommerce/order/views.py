from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from order.models import Order, OrderItem
from order.serializers import (
    OrderReadSerializer,
    OrderWriteSerializer,
    OrderItemSerializer,
)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderReadSerializer
    queryset = Order.objects.all()
    http_method_names = ["get", "post", "delete"]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderWriteSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).order_by("-id")

    def create(self, request, *args, **kwargs):
        serializer = OrderWriteSerializer(
            data=request.data, context={"user_id": request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderItemViewSet(viewsets.ModelViewSet):
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    http_method_names = ["get", "delete"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            order__id=self.kwargs["order_id"], order__user=self.request.user
        )
        return queryset
