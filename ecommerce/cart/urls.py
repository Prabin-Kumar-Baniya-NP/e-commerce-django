from django.urls import path, include
from rest_framework.routers import SimpleRouter
from cart.views import CartViewSet, CartItemViewSet

app_name = "cart"

cart_router = SimpleRouter()
cart_item_router = SimpleRouter()

cart_router.register(r"", CartViewSet, basename="cart")
cart_item_router.register(r"", CartItemViewSet, basename="item")

urlpatterns = [
    path("", include(cart_router.urls)),
    path("item/", include(cart_item_router.urls)),
]
