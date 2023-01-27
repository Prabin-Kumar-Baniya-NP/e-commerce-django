from rest_framework import generics
from product.models import Product
from product.serializers import ProductDetailSerializer, ProductListSerializer
from product.pagination import ProductPagination


class ProductList(generics.ListAPIView):
    serializer_class = ProductListSerializer
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        category_list = self.request.query_params.getlist("category")
        max_price = self.request.query_params.get("max_price")
        min_price = self.request.query_params.get("min_price")
        if category_list is not None:
            for category in category_list:
                queryset = queryset.filter(category__name=category)
        if max_price:
            queryset = queryset.filter(variant__price__lte=max_price)
        if min_price:
            queryset = queryset.filter(variant__price__gte=max_price)
        return queryset


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
