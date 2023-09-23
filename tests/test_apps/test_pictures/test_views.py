import dataclasses
from http import HTTPStatus
from django.urls import reverse
import pytest
from django.test import Client
from server.apps.identity.models import User
from server.apps.pictures.models import FavouritePicture


@pytest.mark.django_db()
def test_favs(authenticated_client: Client) -> None:
    """Test ensures that favs."""
    response = authenticated_client.get(reverse('pictures:favourites'))

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
@pytest.mark.picture_fetch_limit_data(2)
def test_dash(authenticated_client: Client, mock_picture_fetch) -> None:
    """Test ensures that dash."""
    response = authenticated_client.get(reverse('pictures:dashboard'))
    pics = mock_picture_fetch
    assert len(pics) == 2

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db()
def test_dash_new_fav(authenticated_client: Client, mimesis_field) -> None:
    """Test ensures that dash posts."""
    foreign_id = mimesis_field('increment')
    url = mimesis_field('uri')
    response = authenticated_client.post(
        reverse('pictures:dashboard'),
        data={
            'foreign_id': foreign_id,
            'url':  url,
        },
    )
    assert response.status_code == HTTPStatus.FOUND
    assert FavouritePicture.objects.filter(url=url).exists()
    fav = FavouritePicture.objects.get(url=url)
    assert str(fav) == '<Picture {0} by {1}>'.format(
        foreign_id,
        response.wsgi_request.user.id,
    )
