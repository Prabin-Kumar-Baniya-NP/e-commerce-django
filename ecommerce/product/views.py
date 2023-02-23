from django.db.models import Avg, Count
from rest_framework import generics
from product.models import Product
from product.serializers import ProductSerializer
from product.pagination import ProductPagination
from product.filters import ProductFilter


class ProductList(generics.ListAPIView):

    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [ProductFilter]

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        queryset = queryset.annotate(
            rating_average=Avg("product_reviews__rating"),
            rating_count=Count("product_reviews__rating"),
        )
        return queryset


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("category", "variant__inventory", "variant__attribute")
        )
