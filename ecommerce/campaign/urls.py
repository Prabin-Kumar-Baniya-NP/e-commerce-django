from django.urls import path
from campaign import views


app_name = "campaign"

urlpatterns = [
    path("<int:product_id>/", views.campaign_list, name="list"),
    path(
        "check/<int:product_id>/<str:promocode>/", views.check_promocode, name="check"
    ),
]
