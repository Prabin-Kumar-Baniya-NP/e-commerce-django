from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import PermissionDenied
from user.models import Address


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["id", "created_on", "modified_on"]

    def validate_user(self, value):
        if self.context["user"] == value:
            return value
        raise PermissionDenied(
            detail="User id doesn't match with authentation credentials"
        )


class AddressUpdateSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ["id", "user", "created_on", "modified_on"]
