from rest_framework import serializers
from inventory.models import Inventory


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        exclude = ["sold"]


class NestedInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["id", "variant", "available"]
