import factory
from user.tests.factory import UserFactory
from product.tests.factory import ProductFactory


class ReviewsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "reviews.Reviews"

    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    rating = factory.Iterator([4, 1, 5, 2, 3])
    comment = factory.faker.Faker("paragraph")
    is_approved = True
