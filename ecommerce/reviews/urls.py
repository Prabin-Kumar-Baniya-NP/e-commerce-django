from rest_framework.routers import DefaultRouter
from reviews.views import ReviewsViewSet

router = DefaultRouter()

router.register(r"", ReviewsViewSet, "list")

urlpatterns = router.urls
