import pytest
from rest_framework.test import APIClient
from pytest_factoryboy import register
from user.test.factory import UserFactory, AddressFactory
from rest_framework_simplejwt.tokens import RefreshToken

register(UserFactory)
register(AddressFactory)


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
