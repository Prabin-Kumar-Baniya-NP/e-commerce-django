from rest_framework import generics
from reviews.models import Reviews
from rest_framework.permissions import IsAuthenticated
from reviews.serializers import (
    ReviewsReadSerializer,
    ReviewsUpdateSerializer,
    ReviewsWriteSerializer,
)
from drf_spectacular.utils import OpenApiParameter, extend_schema
from drf_spectacular.types import OpenApiTypes


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="product", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY
        ),
        OpenApiParameter(
            name="rating", type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY
        ),
        OpenApiParameter(
            name="user", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY
        ),
    ]
)
class ReviewsList(generics.ListAPIView):
    serializer_class = ReviewsReadSerializer

    def get_queryset(self):
        queryset = Reviews.objects.filter(is_approved=True)
        product = self.request.query_params.get("product")
        rating = self.request.query_params.get("rating")
        user = self.request.query_params.get("user")
        if product:
            queryset = queryset.filter(product__id=product)
        if rating:
            queryset = queryset.filter(rating__lte=rating)
        if user:
            queryset = queryset.filter(user__id=user)
        return queryset


class ReviewsDetail(generics.RetrieveAPIView):
    queryset = Reviews.objects.filter(is_approved=True)
    serializer_class = ReviewsReadSerializer


class ReviewsCreate(generics.CreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsWriteSerializer
    permission_classes = [IsAuthenticated]


class ReviewsUpdate(generics.UpdateAPIView):
    serializer_class = ReviewsUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reviews.objects.filter(user=self.request.user)


class ReviewsDestroy(generics.DestroyAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsWriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reviews.objects.filter(user=self.request.user)


@extend_schema(
    parameters=[
        OpenApiParameter(
            name="product", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY
        ),
    ]
)
class UserReviewsList(generics.ListAPIView):
    serializer_class = ReviewsReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Reviews.objects.filter(user=self.request.user)
        product = self.request.query_params.get("product")
        if product:
            queryset = queryset.filter(product__id=product)
        return queryset


class UserReviewsDetail(generics.RetrieveAPIView):
    serializer_class = ReviewsReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reviews.objects.filter(user=self.request.user)
