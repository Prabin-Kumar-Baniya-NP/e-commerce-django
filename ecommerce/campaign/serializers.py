from rest_framework import serializers
from campaign.models import Campaign


class CampaignReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = [
            "id",
            "name",
            "discount",
            "start_datetime",
            "end_datetime",
            "promocode",
            "auto_apply",
        ]


class NestedCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = [
            "id",
            "name",
            "promocode",
        ]
