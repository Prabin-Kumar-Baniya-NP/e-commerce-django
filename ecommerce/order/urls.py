from rest_framework import routers
from order.views import OrderViewSet, OrderItemViewSet

app_name = "order"

router = routers.SimpleRouter()

router.register("item", OrderItemViewSet, basename="item")
router.register("", OrderViewSet, basename="order")


urlpatterns = router.urls
