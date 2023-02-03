from campaign.models import Campaign
from campaign.serializers import CampaignReadSerializer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def campaign_list(request, product_id):
    now = timezone.now()
    campaign = Campaign.objects.filter(
        product__in=[product_id],
        start_datetime__lte=now,
        end_datetime__gte=now,
        auto_apply=True,
        is_active=True,
    )
    serializer = CampaignReadSerializer(campaign, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_promocode(request, product_id, promocode):
    try:
        campaign = Campaign.objects.get(
            product__in=[product_id], promocode=promocode, is_active=True
        )
    except Campaign.DoesNotExist:
        raise NotFound("Promocode Not Found")

    now = timezone.now()

    if campaign.start_datetime <= now and campaign.end_datetime >= now:
        serializer = CampaignReadSerializer(campaign)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        raise PermissionDenied(detail="Invalid Promocode")
