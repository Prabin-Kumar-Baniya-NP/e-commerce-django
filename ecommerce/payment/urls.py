from rest_framework import routers
from payment import views

app_name = "order"

router = routers.DefaultRouter()
router.register(r"", views.PaymentViewSet, basename="payment")
router.register(r"status", views.PaymentStatusViewSet, basename="status")
router.register(r"stripe", views.StripeViewSet, basename="stripe")
router.register(r"webhook/stripe", views.StripeWebhookViewSet, basename="webhook-stripe")

urlpatterns = router.urls
