from rest_framework import generics
from reviews.models import Reviews
from rest_framework.permissions import IsAuthenticated
from reviews.serializers import (
    ReviewsReadSerializer,
    ReviewsWriteSerializer,
    ReviewsUpdateSerializer,
)
from reviews.permissions import HasObjectOwnership


class ReviewsList(generics.ListAPIView):
    serializer_class = ReviewsReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Reviews.objects.filter(is_approved=True)
        product = self.request.query_params.get("product")
        rating = self.request.query_params.get("rating")
        user = self.request.query_params.get("user")
        if product:
            queryset = queryset.filter(product=product)
        if rating:
            queryset = queryset.filter(rating__lte=rating)
        if user:
            queryset = queryset.filter(user=self.request.user)
        return queryset


class ReviewsDetail(generics.RetrieveAPIView):
    queryset = Reviews.objects.filter(is_approved=True)
    serializer_class = ReviewsReadSerializer
    permission_classes = [IsAuthenticated]


class UserReviewsList(generics.ListAPIView):
    serializer_class = ReviewsReadSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reviews.objects.filter(user=self.request.user)


class ReviewsCreate(generics.CreateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsWriteSerializer
    permission_classes = [IsAuthenticated]


class ReviewsUpdate(generics.UpdateAPIView):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsUpdateSerializer
    permission_classes = [IsAuthenticated, HasObjectOwnership]


class ReviewsDestroy(generics.DestroyAPIView):
    queryset = Reviews.objects.all()
    permission_classes = [IsAuthenticated, HasObjectOwnership]
