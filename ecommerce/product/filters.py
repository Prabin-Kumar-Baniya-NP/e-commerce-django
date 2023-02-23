from rest_framework.filters import BaseFilterBackend
from django.db.models import Min, Max, Avg, Count, Prefetch
from product.models import ProductVariant


class ProductFilter(BaseFilterBackend):
    """
    Filters the Product Variant Queryset based on given params
    """

    def filter_queryset(self, request, queryset, view):
        # Get Query Parameters
        product_name = request.query_params.get("name")
        category_list = request.query_params.getlist("category")
        min_avg_rating = request.query_params.get("min_avg_rating")
        max_price = request.query_params.get("max_price")
        min_price = request.query_params.get("min_price")
        ordering = request.query_params.get("ordering")

        # Apply Filter
        if product_name:
            queryset = queryset.filter(name__icontains = product_name)

        if category_list is not None:
            for category in category_list:
                queryset = queryset.filter(category__id=int(category))

        if max_price and min_price:
            queryset = queryset.prefetch_related(
                Prefetch(
                    "variant",
                    queryset=ProductVariant.objects.filter(
                        price__gte=min_price, price__lte=max_price
                    ).order_by("-price" if ordering == "price_desc" else "price"),
                )
            )
        elif max_price:
            queryset = queryset.prefetch_related(
                Prefetch(
                    "variant",
                    queryset=ProductVariant.objects.filter(
                        price__lte=max_price
                    ).order_by("-price"),
                )
            )
        elif min_price:
            queryset = queryset.prefetch_related(
                Prefetch(
                    "variant",
                    queryset=ProductVariant.objects.filter(
                        price__gte=min_price
                    ).order_by("price"),
                )
            )
        else:
            queryset = queryset.prefetch_related(
                Prefetch(
                    "variant",
                    queryset=ProductVariant.objects.all().order_by(
                        "-price" if ordering == "price_desc" else "price"
                    ),
                )
            )

        if min_avg_rating:
            queryset = queryset.annotate(
                avg_rating=Avg("product_reviews__rating")
            ).filter(avg_rating__gte=min_avg_rating)

        # Apply ordering
        if ordering == "reviews_asc":
            queryset = queryset.order_by("rating_count")

        if ordering == "reviews_desc":
            queryset = queryset.order_by("-rating_count")

        if ordering == "price_asc":
            queryset = queryset.annotate(
                min_variant_price=Min("variant__price")
            ).order_by("min_variant_price")

        if ordering == "price_desc":
            queryset = queryset.annotate(
                max_variant_price=Max("variant__price")
            ).order_by("-max_variant_price")

        return queryset.prefetch_related(
            "category", "variant__attribute", "variant__inventory"
        )
