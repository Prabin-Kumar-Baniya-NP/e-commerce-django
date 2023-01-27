from django.urls import path
from reviews import views

app_name = "reviews"

urlpatterns = [
    path("", views.ReviewsList.as_view(), name="list"),
    path("user/", views.UserReviewsList.as_view(), name="user-reviews-list"),
    path("create/", views.ReviewsCreate.as_view(), name="create"),
    path("update/<int:pk>/", views.ReviewsUpdate.as_view(), name="update"),
    path("delete/<int:pk>/", views.ReviewsDestroy.as_view(), name="delete"),
]
