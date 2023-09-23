import dataclasses
from http import HTTPStatus
from django.urls import reverse
import pytest
from django.test import Client
from server.apps.identity.models import User


@pytest.mark.django_db()
def test_login(client: Client) -> None:
    """Test ensures that app urls are accessible."""
    response = client.get(reverse('identity:login'))

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_registration(client: Client, mock_lead_create, user_registration_data) -> None:
    """Test ensures registration works."""
    user = user_registration_data
    response = client.post(
        reverse('identity:registration'),
        data=dataclasses.asdict(user),
    )
    assert response.status_code == HTTPStatus.FOUND
    user = User.objects.get(email=user.email)
    assert user.lead_id == int(mock_lead_create)


@pytest.mark.django_db()
def test_user_update(client: Client, mock_lead_update, user_factory, mimesis_field) -> None:
    """Test ensures registration works."""
    lead_id = '2'
    user = user_factory(lead_id=int(lead_id))
    client.force_login(user=user)
    new_date_of_birth = mimesis_field('date')

    response = client.post(
        reverse('identity:user_update'),
        data={
            'date_of_birth': new_date_of_birth.strftime('%Y-%m-%d'),
            'first_name': user.first_name,
            'last_name': user.last_name,
            'address': user.address,
            'job_title': user.job_title,
            'phone': user.phone,
        },
    )
    assert response.status_code == HTTPStatus.FOUND
    user = User.objects.get(email=user.email)
    assert user.date_of_birth == new_date_of_birth
    assert mock_lead_update.last_request().url.endswith(lead_id)
