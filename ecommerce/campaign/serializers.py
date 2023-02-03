from rest_framework import serializers
from campaign.models import Campaign


class CampaignReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campaign
        fields = [
            "name",
            "discount",
            "start_datetime",
            "end_datetime",
            "promocode",
            "auto_apply",
        ]
