import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "user.User"

    first_name = factory.faker.Faker("first_name")
    middle_name = factory.faker.Faker("first_name")
    last_name = factory.faker.Faker("last_name")
    password = "test_user@12345"
    date_of_birth = "2000-01-01"
    gender = factory.Iterator(["M", "F"])
    email = factory.faker.Faker("email")
    is_email_verified = False
    phone_number = factory.faker.Faker("phone_number")
    is_phone_number_verified = False
    image = ""
    date_joined = factory.faker.Faker("date_time")
    last_updated = factory.faker.Faker("date_time")
    is_active = True
    is_staff = False
    is_superuser = False


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "user.Address"

    user = factory.SubFactory(UserFactory)
    type = factory.Iterator(["H", "W", "O"])
    house_number = factory.faker.Faker("building_number")
    landmark = factory.faker.Faker("street_name")
    address_line1 = factory.faker.Faker("street_address")
    address_line2 = factory.faker.Faker("street_address")
    city = factory.faker.Faker("city")
    state = factory.faker.Faker("city")
    country = factory.faker.Faker("country")
    postal_code = factory.faker.Faker("postcode")
    is_default = False
    created_on = factory.faker.Faker("date_time")
    modified_on = factory.faker.Faker("date_time")
