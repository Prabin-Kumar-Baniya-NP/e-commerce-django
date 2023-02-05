from django.urls import path
from rest_framework import routers
from product import views


app_name = "product"

router = routers.SimpleRouter()
router.register(r"product", views.ProductList, "list"),

urlpatterns = [
    path("", views.ProductList.as_view(), name="list"),
    path("<int:pk>/", views.ProductDetail.as_view(), name="detail"),
    path("variant/", views.ProductVariantList.as_view(), name="variant-list"),
    path("rating/", views.ProductRatingList.as_view(), name="rating-list"),
    path("rating/<int:pk>/", views.ProductRatingDetail.as_view(), name="rating-detail"),
]
