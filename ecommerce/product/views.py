from rest_framework import generics
from product.models import Product
from product.serializers import ProductSerializer
from product.pagination import ProductPagination
from product.filter import ProductSearchFilter


class ProductList(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    filter_backends = [ProductSearchFilter]


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
