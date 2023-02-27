import factory
from user.tests.factory import UserFactory
from product.tests.factory import ProductVariantFactory
from campaign.tests.factory import CampaignFactory


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "cart.Cart"

    user = factory.SubFactory(UserFactory)


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "cart.CartItem"

    cart = factory.SubFactory(CartFactory)
    variant = factory.SubFactory(ProductVariantFactory)
    campaign = factory.SubFactory(CampaignFactory)
    quantity = factory.Iterator([1, 2, 3, 4])
