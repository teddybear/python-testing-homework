from django.test import Client
import pytest
from mimesis import Field, Locale


@pytest.fixture()
def authenticated_client(user_factory, client: Client):
    user = user_factory()
    client.force_login(user=user)
    yield client
    user.delete()


@pytest.fixture()
def mimesis_field():
    return Field(Locale.RU)
