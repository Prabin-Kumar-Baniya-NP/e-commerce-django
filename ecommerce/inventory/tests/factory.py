import factory
from product.tests.factory import ProductVariantFactory


class InventoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "inventory.Inventory"

    variant = factory.SubFactory(ProductVariantFactory)
    available = factory.Iterator([10, 20, 30])
    sold = factory.Iterator([5, 15, 25])
