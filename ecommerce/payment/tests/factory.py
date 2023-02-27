import factory
from decimal import Decimal


class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "payment.Payment"

    provider = "STRIPE"
    status = "REQUESTED"
    amount_requested = factory.Iterator([Decimal(100.00), Decimal(1000.00)])
    amount_paid = factory.Iterator([Decimal(100.00), Decimal(1000.00)])
