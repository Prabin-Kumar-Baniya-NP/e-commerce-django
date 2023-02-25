import pytest
from rest_framework.test import APIClient
from pytest_factoryboy import register
from user.tests.factory import UserFactory
from rest_framework_simplejwt.tokens import RefreshToken

register(UserFactory)


import pytest


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Enable database access for all tests.
    """
    pass


pytest.mark.django_db = enable_db_access_for_all_tests


@pytest.fixture
def anonymous_client():
    client = APIClient()
    return client


@pytest.fixture
def authenticated_client(user_factory):
    user = user_factory.create()
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client


@pytest.fixture
def user_client(user_factory):
    user = user_factory.create()
    refresh = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return [user, client]
