import factory


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "category.Category"

    name = factory.faker.Faker("name")
    description = factory.faker.Faker("paragraph")
    is_active = True
