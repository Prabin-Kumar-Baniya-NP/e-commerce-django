from rest_framework import generics
from category.models import Category
from category.pagination import CategoryPagination
from category.serializers import CategoryListSerializer, CategoryDetailSerializer


class CategoryList(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True).order_by("name")
    serializer_class = CategoryListSerializer
    pagination_class = CategoryPagination


class CategoryDetail(generics.RetrieveAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategoryDetailSerializer
