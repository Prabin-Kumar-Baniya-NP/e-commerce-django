from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from reviews.models import Reviews
from reviews.serializers import (
    ReviewsSerializer,
    ReviewsCreateSerializer,
    ReviewUpdateSerializer,
)
from rest_framework.response import Response


class ReviewsViewSet(viewsets.ModelViewSet):
    """
    Viewset for CRUD operation on reviews
    """

    def list(self, request):
        queryset = Reviews.objects.filter(is_approved=True)
        serializer = ReviewsSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ReviewsCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk):
        review = Reviews.objects.get(id=pk)
        serializer = ReviewsSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        review = Reviews.objects.get(id=pk)
        serializer = ReviewsSerializer(review, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        review = Reviews.objects.get(id=pk)
        serializer = ReviewsSerializer(review, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        pass
