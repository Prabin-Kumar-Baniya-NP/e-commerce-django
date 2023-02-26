import pytest


@pytest.fixture
def inventory(inventory_factory):
    return inventory_factory.create()
