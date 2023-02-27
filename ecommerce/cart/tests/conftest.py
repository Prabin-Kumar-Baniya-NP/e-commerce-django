import pytest


@pytest.fixture
def cart_client(user_client, cart_factory, cart_item_factory):
    """
    Returns cart filled with an item and client associated with that cart
    """
    user, client = user_client
    cart = cart_factory.create(user=user)
    cart_item_factory.create(cart=cart)
    return [cart, client]

@pytest.fixture
def cart_item_client(user_client, cart_factory, cart_item_factory):
    """
    Returns cart item and client associated with that cart item
    """
    user, client = user_client
    cart = cart_factory.create(user=user)
    cart_item = cart_item_factory.create(cart=cart)
    return [cart_item, client]
