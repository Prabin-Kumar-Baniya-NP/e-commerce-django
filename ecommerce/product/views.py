from rest_framework import generics
from product.models import Product, ProductVariant
from product.serializers import ProductSerializer, VariantListSerializer
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


class ProductVariantList(generics.ListAPIView):
    queryset = ProductVariant.objects.filter(is_active=True)
    serializer_class = VariantListSerializer
    filter_backends = [VariantSearchFilter]
