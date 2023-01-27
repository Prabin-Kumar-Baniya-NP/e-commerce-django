from rest_framework.serializers import ModelSerializer
from user.models import Address


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["id", "created_on", "modified_on"]


class AddressUpdateSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["id", "user", "created_on", "modified_on"]
