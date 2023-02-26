import factory
from decimal import Decimal
from datetime import timedelta
from django.utils.timezone import now


class CampaignFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "campaign.Campaign"

    name = factory.faker.Faker("name")
    description = factory.faker.Faker("paragraph")
    discount = factory.Iterator([Decimal(10.50), Decimal(15.55), Decimal(12.19)])
    start_datetime = now()
    end_datetime = now() + timedelta(days=2)
    promocode = factory.faker.Faker("name")
    auto_apply = True
    is_active = True

    @factory.post_generation
    def product(self, create, extracted):
        """
        Adds product to the campaign by extracting product from extracted.
        """
        if not create:
            return

        if extracted:
            for product in extracted:
                self.product.add(product)
