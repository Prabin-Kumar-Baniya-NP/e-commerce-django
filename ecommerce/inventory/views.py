from inventory.serializers import InventorySerializer
from inventory.models import Inventory
from rest_framework.generics import RetrieveAPIView


class InventoryDetail(RetrieveAPIView):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()
    lookup_field = "variant"
