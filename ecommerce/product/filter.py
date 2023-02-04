from rest_framework.filters import BaseFilterBackend
from django.db.models import Avg, Max, Min, Count
from product.models import Product


class VariantSearchFilter(BaseFilterBackend):
    """
    Filters the Product Variant Queryset based on given params
    """

    def filter_queryset(self, request, queryset, view):
        # Get Query Parameters
        category_list = request.query_params.getlist("category")
        min_avg_rating = request.query_params.get("min_avg_rating")
        max_price = request.query_params.get("max_price")
        min_price = request.query_params.get("min_price")
        ordering = request.query_params.get("ordering")

        # Apply Filter
        if category_list is not None:
            for category in category_list:
                queryset = queryset.filter(product__category__id=int(category))

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if min_avg_rating:
            queryset = queryset.filter(
                product__in=Product.objects.annotate(
                    avg_rating=Avg("product_reviews__rating")
                )
                .filter(avg_rating__gte=min_avg_rating)
                .only("id")
            )

        # Apply Ordering
        if ordering == "price_asc":
            queryset = queryset.order_by("price")

        if ordering == "price_desc":
            queryset = queryset.order_by("-price")

        if ordering == "reviews_asc":
            queryset = (
                queryset.annotate()
                .annotate(reviews_count=Count("product__product_reviews"))
                .order_by("reviews_count")
            )

        if ordering == "reviews_desc":
            queryset = (
                queryset.annotate()
                .annotate(reviews_count=Count("product__product_reviews"))
                .order_by("-reviews_count")
            )

        return queryset.select_related("product").prefetch_related("inventory", "attribute")
