import factory
from decimal import Decimal


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "product.Product"

    name = factory.faker.Faker("name")
    description = factory.faker.Faker("paragraph")
    is_active = True

    @factory.post_generation
    def category(self, create, extracted):
        """
        Adds category to the product by extracting category from extracted.
        """
        if not create:
            return

        if extracted:
            for category in extracted:
                self.category.add(category)


# product = ProductFactory.create(category=[CategoryFactory() for i in range(5)])


class ProductArributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "product.ProductAttribute"

    name = "COLOR"
    value = factory.faker.Faker("color_name")


class ProductVariantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "product.ProductVariant"

    product = factory.SubFactory(ProductFactory)
    sku = factory.faker.Faker("ssn")
    price = factory.Iterator(
        [Decimal(12.12), Decimal(8.55), Decimal(15.55), Decimal(2.22)]
    )
    currency = "USD"
    is_active = True

    @factory.post_generation
    def attribute(self, create, extracted):
        """
        Adds attribute to the product by extracting attribute from extracted.
        """
        if not create:
            return

        if extracted:
            for attribute in extracted:
                self.attribute.add(attribute)


# variant = ProductVariantFactory.create(attribute=[ProductArributeFactory() for i in range(5)])
