from rest_framework.reverse import reverse
from campaign.serializers import CampaignReadSerializer
from campaign.models import Campaign
from datetime import timedelta
from django.utils.timezone import now


def test_campaign_list(campaign, anonymous_client):
    product = campaign.product.all()[0]
    response = anonymous_client.get(
        reverse("campaign:list", kwargs={"product_id": product.id})
    )
    assert response.status_code == 200
    serializer = CampaignReadSerializer([campaign], many=True)
    assert response.data == serializer.data


def test_valid_promocode(campaign, anonymous_client):
    product = campaign.product.all()[0]
    response = anonymous_client.get(
        reverse(
            "campaign:check",
            kwargs={"product_id": product.id, "promocode": campaign.promocode},
        )
    )
    assert response.status_code == 200


def test_unknown_promocode(campaign, anonymous_client):
    product = campaign.product.all()[0]
    response = anonymous_client.get(
        reverse(
            "campaign:check",
            kwargs={
                "product_id": product.id,
                "promocode": campaign.promocode + "invalid",
            },
        )
    )
    assert response.status_code == 404


def test_invalid_promocode(campaign, anonymous_client):
    product = campaign.product.all()[0]
    Campaign.objects.filter(id=campaign.id).update(
        start_datetime=now() + timedelta(days=1), end_datetime=now() + timedelta(days=3)
    )
    response = anonymous_client.get(
        reverse(
            "campaign:check",
            kwargs={"product_id": product.id, "promocode": campaign.promocode},
        )
    )
    assert response.status_code == 403
