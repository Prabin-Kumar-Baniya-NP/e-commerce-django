from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from inventory.serializers import InventoryReadSerializer
from inventory.models import Inventory


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def inventory_detail(request, variant_id):
    try:
        inventory = Inventory.objects.get(variant = variant_id)
    except Inventory.DoesNotExist:
        raise NotFound("Inventory Not Found")
    
    serializer = InventoryReadSerializer(inventory)
    return Response(serializer.data, status = status.HTTP_200_OK)
