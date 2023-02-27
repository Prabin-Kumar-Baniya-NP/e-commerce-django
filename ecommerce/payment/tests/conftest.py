import pytest

@pytest.fixture
def payment_client(user_client, address_factory, order_factory, order_item_factory, payment_factory):
    """
    Returns payment and client associated with the payment
    """
    user, client = user_client
    address = address_factory.create(user=user)
    order = order_factory.create(user=user, shipping_address=address)
    order_item = order_item_factory.create(order=order)
    payment = payment_factory.create(order=order)
    return [payment, client]
