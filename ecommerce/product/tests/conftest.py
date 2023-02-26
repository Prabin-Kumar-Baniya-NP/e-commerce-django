import pytest


@pytest.fixture
def product(product_factory):
    """
    Returns product object
    """
    return product_factory.create()
