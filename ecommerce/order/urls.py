from django.urls import path, include
from rest_framework import routers
from order.views import OrderViewSet, OrderItemViewSet

app_name = "order"

order_router = routers.SimpleRouter()
order_item_router = routers.SimpleRouter()

order_router.register("", OrderViewSet, basename="order")
order_item_router.register("", OrderItemViewSet, basename="item")


urlpatterns = [
    path("", include(order_router.urls)),
    path("<int:order_id>/item/", include(order_item_router.urls)),
]
