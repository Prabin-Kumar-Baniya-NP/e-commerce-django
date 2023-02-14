from rest_framework import serializers
from payment.models import Payment


class PaymentReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
