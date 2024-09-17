from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from cart.serializers import CartSerializer, CartItemSerializer
from cart.models import Cart, CartItem


class CartViewSet(viewsets.GenericViewSet):
    """
    Viewset for getting and clearing cart of the user
    """

    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_cart_object(self):
        cart, created = Cart.objects.prefetch_related("item").get_or_create(user=self.request.user)
        return cart

    @action(methods=["GET"], detail=False, url_path="get", url_name="get")
    def get_cart(self, request, *args, **kwargs):
        """
        Returns the cart of the user
        """
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(self.get_cart_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["DELETE"], detail=False, url_path="clear", url_name="clear")
    def clear_cart(self, request, *args, **kwargs):
        """
        Clears the cart of the user
        """
        count, deleted = CartItem.objects.filter(cart=self.get_cart_object()).delete()
        return Response({"count": count}, status=status.HTTP_204_NO_CONTENT)


class CartItemViewSet(viewsets.ModelViewSet):
    """
    Viewset for creating, updating, reading and deleting cart item information
    """

    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get_cart_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def get_object(self):
        return CartItem.objects.get(id=self.kwargs["pk"], cart=self.request.user.cart)

    def get_queryset(self):
        cart = Cart.objects.get(user_id = self.request.user.id)
        return CartItem.objects.filter(cart_id = cart.id)
