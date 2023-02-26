import pytest


@pytest.fixture
def campaign(campaign_factory, product_factory):
    """
    Returns campaign object
    """
    return campaign_factory.create(product=[product_factory.create()])
