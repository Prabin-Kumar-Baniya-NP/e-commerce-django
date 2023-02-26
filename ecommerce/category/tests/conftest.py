import pytest

@pytest.fixture
def category(category_factory):
    """
    Returns category object
    """
    return category_factory.create()
