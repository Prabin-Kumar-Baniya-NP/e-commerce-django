import pytest


@pytest.fixture
def reviews(reviews_factory):
    """
    Returns reviews object
    """
    return reviews_factory.create()


@pytest.fixture
def reviews_client(user_client, reviews_factory):
    """
    Returns reviews and client
    """
    user, client = user_client
    reviews = reviews_factory.create(user=user)
    return [reviews, client]
