import pytest
from server.apps.identity.models import User


@pytest.mark.django_db()
def test_create_user_without_email():
    """Check if raises error on no email."""
    with pytest.raises(ValueError):
        User.objects.create_user(email=None, password='')
