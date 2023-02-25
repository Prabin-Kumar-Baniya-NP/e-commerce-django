import pytest
from pytest_factoryboy import register
from user.tests.factory import AddressFactory

register(AddressFactory)


@pytest.fixture
def address_client(user_client, address_factory):
    user, client = user_client
    address = address_factory(user=user)
    return [address, client]
