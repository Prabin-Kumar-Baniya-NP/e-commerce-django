from rest_framework.routers import DefaultRouter
from cart.views import CartViewSet, CartItemViewSet

app_name = "cart"

router = DefaultRouter()
router.register(r"", CartViewSet, basename="cart")
router.register(r"item", CartItemViewSet, basename="item")

urlpatterns = router.urls
