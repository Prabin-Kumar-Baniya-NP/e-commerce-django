from campaign.models import Campaign
from campaign.serializers import CampaignReadSerializer
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.decorators import api_view
from django.utils import timezone
from ecommerce.serializers import HTTP4XXExceptionSerializer
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiExample,
)
from drf_spectacular.types import OpenApiTypes


@extend_schema(
    description="Retrieve a list of campaigns for a given product ID.",
    parameters=[
        OpenApiParameter(
            name="product_id",
            description="Id of given product",
            location=OpenApiParameter.PATH,
            type=OpenApiTypes.INT,
        )
    ],
    responses=CampaignReadSerializer(many=True),
)
@api_view(["GET"])
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


@extend_schema(
    description="Checks the promocode for given product id",
    parameters=[
        OpenApiParameter(
            name="product_id",
            description="Id of given product",
            location=OpenApiParameter.PATH,
            type=OpenApiTypes.INT,
        ),
        OpenApiParameter(
            name="promocode",
            description="Promocode value of the campaign",
            location=OpenApiParameter.PATH,
            type=OpenApiTypes.STR,
        ),
    ],
    responses={
        200: OpenApiResponse(
            response=CampaignReadSerializer,
            description="Campaign Description",
        ),
        403: OpenApiResponse(
            response=HTTP4XXExceptionSerializer,
            description="Promocode Currently Unavailable",
            examples=[
                OpenApiExample(
                    "invalid promocode",
                    value={
                        "detail": "Promocode Currently Unavailable",
                    },
                    status_codes=[403],
                    response_only=True,
                ),
            ],
        ),
        404: OpenApiResponse(
            response=HTTP4XXExceptionSerializer,
            description="Promocode Not Found",
            examples=[
                OpenApiExample(
                    "Promocode Not Found",
                    value={
                        "detail": "Promocode Not Found",
                    },
                    status_codes=[404],
                    response_only=True,
                ),
            ],
        ),
    },
)
@api_view(["GET"])
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
    raise PermissionDenied(detail="Promocode Currently Unavailable")
