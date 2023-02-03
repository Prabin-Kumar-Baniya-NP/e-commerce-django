from rest_framework import serializers
from inventory.models import Inventory


class InventoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["variant", "available"]
