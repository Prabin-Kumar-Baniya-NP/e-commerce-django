from django.db.models import Avg, Count
from rest_framework import generics
from product.models import Product
from product.serializers import ProductSerializer
from product.pagination import ProductPagination
from product.filters import ProductFilter
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="name",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
        ),
        OpenApiParameter(
            name="category",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            
        ),
        OpenApiParameter(
            name="min_avg_rating",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            
        ),
        OpenApiParameter(
            name="max_price",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            
        ),
        OpenApiParameter(
            name="min_price",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            
        ),
        OpenApiParameter(
            name="ordering",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            
        ),
    ]
)
class ProductList(generics.ListAPIView):
    """
    Lists the products
    """

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
