import factory
from decimal import Decimal
from product.tests.factory import ProductVariantFactory


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "order.Order"

    status = "CREATED"
    total_price = factory.Iterator(
        [Decimal(1000.00), Decimal(2000.00), Decimal(3000.00)]
    )
    currency = "USD"


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "order.OrderItem"

    variant = factory.SubFactory(ProductVariantFactory)
    quantity = factory.Iterator([1, 5, 10])
    final_price = factory.Iterator([Decimal(100.00), Decimal(200.00), Decimal(300.00)])
