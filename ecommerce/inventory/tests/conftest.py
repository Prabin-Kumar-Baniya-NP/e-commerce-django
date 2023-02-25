import pytest
from pytest_factoryboy import register
from inventory.tests.factory import InventoryFactory

register(InventoryFactory)

@pytest.fixture
def inventory():
    return InventoryFactory.create()
