import json
from http import HTTPStatus
from typing import TYPE_CHECKING
from urllib.parse import urljoin

import httpretty
import pytest
from django_fakery.faker_factory import Factory
from mimesis import Field, Locale

from server.apps.pictures.models import FavouritePicture

if TYPE_CHECKING:
    from server.common.django.types import Settings


@pytest.fixture()
def user_fav_factory(
    fakery: Factory[FavouritePicture],
    user_factory,
):
    """Mock user fav."""
    def decorator(**fields) -> FavouritePicture:
        fields.setdefault('user', user_factory())
        return fakery.m(
            FavouritePicture,
        )(
            **fields,
        )

    return decorator


@pytest.fixture()
def user_favs_factory(
    user_fav_factory,
):
    """Mock user favs."""
    def decorator(nfavs: int = 1, **fields) -> FavouritePicture:
        return [user_fav_factory(**fields) for _ in range(nfavs)]

    return decorator


@pytest.fixture()
def picture_response():
    """Mock PictureFetch response."""
    def factory(limit=1):
        mf = Field(locale=Locale.RU)
        return [
            {
                'id': str(mf('numeric.increment')),
                'url': mf('internet.uri'),
            } for _ in range(limit)
        ]
    return factory


@pytest.fixture()
def mock_picture_fetch(request, settings: 'Settings', picture_response):
    """Mock PictureFetch call."""
    marker = request.node.get_closest_marker('picture_fetch_limit_data')
    limit = marker.args[0]
    resp = picture_response(limit=limit)
    with httpretty.enabled(allow_net_connect=False):
        httpretty.register_uri(
            httpretty.GET,
            urljoin(
                settings.PLACEHOLDER_API_URL,
                'photos',
            ),
            status=HTTPStatus.OK,
            body=json.dumps(resp),
        )
        yield resp
        assert httpretty.has_request()


@pytest.fixture()
def _override_placeholder_api(settings: 'Settings'):
    """Override PLACEHOLDER_API_URL to user json-server."""
    before = settings.PLACEHOLDER_API_URL
    settings.PLACEHOLDER_API_URL = 'http://localhost:3000/'
    yield
    settings.PLACEHOLDER_API_URL = before
