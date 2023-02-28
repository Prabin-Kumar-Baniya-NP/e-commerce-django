from rest_framework import serializers
from campaign.models import Campaign


class CampaignReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        exclude = [
            "description",
            "product",
            "is_active",
        ]


class NestedCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = [
            "id",
            "name",
            "promocode",
        ]
