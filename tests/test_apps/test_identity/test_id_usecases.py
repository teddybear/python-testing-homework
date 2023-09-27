import pytest

from server.apps.identity.container import container
from server.apps.identity.logic.usecases.user_create_new import UserCreateNew
from server.apps.identity.logic.usecases.user_update import UserUpdate
from server.apps.identity.models import User


@pytest.mark.django_db()
def test_create_user(user_factory):
    """Test user creation."""
    user = user_factory()

    assert user.is_active


@pytest.mark.django_db()
def test_create_new_user(user_factory, mock_lead_create):
    """Test create new user with lead."""
    user_create_new = container.instantiate(UserCreateNew)
    user = user_factory()

    user_create_new(user)

    user = User.objects.get(email=user.email)
    assert user.lead_id == int(mock_lead_create)


@pytest.mark.django_db()
def test_update_user_lead(user_factory, mock_lead_update):
    """Test update user lead."""
    lead_id = '2'
    user_update = container.instantiate(UserUpdate)
    user = user_factory(lead_id=int(lead_id))

    user_update(user)
    assert mock_lead_update.last_request().url.endswith(lead_id)


@pytest.mark.usefixtures('_override_placeholder_api')
@pytest.mark.django_db()
def test_create_new_user_json_server(user_factory):
    """Test create new user with lead, real json server."""
    user_create_new = container.instantiate(UserCreateNew)
    user = user_factory()

    user_create_new(user)

    user = User.objects.get(email=user.email)
    assert user.lead_id == 1
