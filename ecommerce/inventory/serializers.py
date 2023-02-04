from rest_framework import serializers
from inventory.models import Inventory


class InventoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["id", "variant", "available", "created_at", "modified_at"]


class NestedInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["available"]
