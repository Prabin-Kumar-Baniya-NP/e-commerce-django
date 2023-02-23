from django.urls import path
from inventory import views

app_name = "inventory"


urlpatterns = [
    path("<int:variant>/", views.InventoryDetail.as_view(), name="detail"),
]
