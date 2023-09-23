import pytest

from server.apps.pictures.container import container
from server.apps.pictures.logic.usecases.favourites_list import FavouritesList
from server.apps.pictures.logic.usecases.pictures_fetch import PicturesFetch


@pytest.mark.django_db()
def test_list_favs(user_favs_factory, user_factory):
    """Test favs list."""
    user = user_factory()
    user_favs_factory(user=user)
    list_favourites = container.instantiate(FavouritesList)

    user_favs = list_favourites(user.id)

    assert len(user_favs) == 1


@pytest.mark.django_db()
@pytest.mark.picture_fetch_limit_data(2)
def test_fetch_picture(mock_picture_fetch):
    """Test fetch picture."""
    fetch = container.instantiate(PicturesFetch)

    fetched = fetch(limit=2)

    assert len(fetched) == 2
    pics = mock_picture_fetch
    assert len(fetched) == len(pics)


@pytest.mark.django_db()
def test_fetch_picture_json_server(_override_placeholder_api):
    """Test create new user with lead, real json server."""
    fetch = container.instantiate(PicturesFetch)

    fetched = fetch(limit=1)

    assert len(fetched) == 1
