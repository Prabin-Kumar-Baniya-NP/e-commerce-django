from rest_framework.filters import BaseFilterBackend
from django.db.models import Avg, Max, Min, Count


class ProductSearchFilter(BaseFilterBackend):
    """
    Filters the Product Queryset based on given params
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
                queryset = queryset.filter(category__id=int(category))

        if max_price:
            queryset = queryset.filter(variant__price__lte=max_price)

        if min_price:
            queryset = queryset.filter(variant__price__gte=max_price)

        if min_avg_rating:
            queryset = (
                queryset.filter(product_reviews__is_approved=True)
                .annotate(avg_rating=Avg("product_reviews__rating"))
                .filter(avg_rating__gte=min_avg_rating)
            )

        # Apply Ordering
        if ordering == "price_asc":
            queryset = queryset.annotate(
                product_variant_price=Min("variant__price")
            ).order_by("product_variant_price")

        if ordering == "price_desc":
            queryset = queryset.annotate(
                product_variant_price=Max("variant__price")
            ).order_by("-product_variant_price")

        if ordering == "reviews_asc":
            queryset = (
                queryset.annotate()
                .annotate(reviews_count=Count("product_reviews"))
                .order_by("reviews_count")
            )

        if ordering == "reviews_desc":
            queryset = (
                queryset.annotate()
                .annotate(reviews_count=Count("product_reviews"))
                .order_by("-reviews_count")
            )

        return queryset.prefetch_related(
            "category", "variant__inventory", "variant__attribute"
        )
