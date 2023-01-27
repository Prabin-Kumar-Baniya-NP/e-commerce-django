from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from user import views

app_name = "user"

urlpatterns = [
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("address/", views.list_address, name="list-address"),
    path("address/<int:id>/", views.get_address, name="get-address"),
    path("address/create/", views.create_address, name="create-address"),
    path("address/update/<int:id>/", views.update_address, name="update-address"),
    path("address/delete/<int:id>/", views.delete_address, name="delete-address"),
]
