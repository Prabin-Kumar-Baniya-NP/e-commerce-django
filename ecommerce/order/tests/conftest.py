import pytest


@pytest.fixture
def order_client(user_client, address_factory, order_factory, order_item_factory):
    """
    Returns order filled with order item and client associated with that order
    """
    user, client = user_client
    address = address_factory.create(user=user)
    order = order_factory.create(user=user, shipping_address=address)
    order_item = order_item_factory.create(order=order)
    return [order, client]
