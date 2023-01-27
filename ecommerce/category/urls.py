from django.urls import path
from category import views

urlpatterns = [
    path("", views.CategoryList.as_view(), name="list"),
    path("<int:pk>/", views.CategoryDetail.as_view(), name="list"),
]
