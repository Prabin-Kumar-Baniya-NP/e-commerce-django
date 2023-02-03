from django.urls import path
from inventory import views

app_name = "inventory"


urlpatterns = [
    path("<int:variant_id>/", views.inventory_detail, name="detail"),
]
