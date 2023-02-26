import pytest


@pytest.fixture
def address_client(user_client, address_factory):
    """
    Returns address and client
    """
    user, client = user_client
    address = address_factory(user=user)
    return [address, client]
