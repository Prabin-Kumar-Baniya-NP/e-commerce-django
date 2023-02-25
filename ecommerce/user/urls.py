from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)
from user import views

app_name = "user"

urlpatterns = [
    path("auth/signup/", views.signup, name="signup"),
    path("auth/update/", views.update_user, name="update"),
    path("auth/detail/", views.user_detail, name="detail"),
    path("auth/verify/email/", views.verify_email, name="verify-email"),
    path("auth/verify/phonenumber/", views.verify_number, name="verify-phone-number"),
    path("auth/password/reset/", views.reset_password, name="reset-password"),
    path("auth/password/change/", views.change_password, name="change-password"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/token/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("address/", views.list_address, name="list-address"),
    path("address/<int:id>/", views.get_address, name="get-address"),
    path("address/create/", views.create_address, name="create-address"),
    path("address/update/<int:id>/", views.update_address, name="update-address"),
    path("address/delete/<int:id>/", views.delete_address, name="delete-address"),
]
