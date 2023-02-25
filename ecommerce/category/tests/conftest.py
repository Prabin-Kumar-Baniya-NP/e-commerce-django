import pytest
from category.tests.factory import CategoryFactory
from pytest_factoryboy import register

register(CategoryFactory)


@pytest.fixture
def category(category_factory):
    return category_factory.create()
