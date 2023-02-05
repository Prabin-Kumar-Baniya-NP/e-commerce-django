from django.db.models import Avg, Count
from rest_framework import generics
from product.models import Product, ProductVariant
from product.serializers import (
    ProductSerializer,
    VariantListSerializer,
    ProductRatingSerializer,
)
from product.pagination import ProductPagination
from product.filter import VariantSearchFilter


class ProductList(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        category_list = self.request.query_params.getlist("category")
        if category_list is not None:
            for category in category_list:
                queryset = queryset.filter(category__id=int(category))
        return queryset.prefetch_related(
            "category", "variant__inventory", "variant__attribute"
        )


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related("category", "variant__inventory", "variant__attribute")
        )


class ProductVariantList(generics.ListAPIView):
    queryset = ProductVariant.objects.filter(is_active=True)
    serializer_class = VariantListSerializer
    filter_backends = [VariantSearchFilter]


class ProductRatingList(generics.ListAPIView):
    serializer_class = ProductRatingSerializer

    def get_queryset(self):
        id_list = self.request.query_params.getlist("id")
        id_list = [int(product_id) for product_id in id_list]
        queryset = (
            Product.objects.filter(id__in=id_list)
            .annotate(
                average=Avg("product_reviews__rating"),
                count=Count("product_reviews__rating"),
            )
            .values("id", "average", "count")
        )
        return queryset


class ProductRatingDetail(generics.RetrieveAPIView):
    serializer_class = ProductRatingSerializer

    def get_object(self):
        obj = (
            Product.objects.annotate(
                average=Avg("product_reviews__rating"),
                count=Count("product_reviews__rating"),
            )
            .values("id", "average", "count")
            .get(id=self.kwargs["pk"])
        )
        return obj
