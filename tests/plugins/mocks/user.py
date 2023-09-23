from dataclasses import dataclass

import pytest
from django_fakery.faker_factory import Factory
from faker import Faker
from mimesis import Field, Locale
from polyfactory.factories import DataclassFactory

from server.apps.identity.models import User


@pytest.fixture()
def user_factory(fakery: Factory[User], faker: Faker):
    """Fixture to create your own custom users. Everything is customizable."""

    def factory(user: User, password: str) -> User:
        # We store the original password for test purposes only:
        user._password = password  # noqa: WPS437
        return user

    def decorator(**fields) -> User:
        password = fields.setdefault('password', faker.password())
        return fakery.m(
            User,
            post_save=[lambda user: factory(user, password)],
        )(
            **{'is_active': True, **fields},
        )

    return decorator


@dataclass
class UserData(object):
    """User Data."""

    email: str
    first_name: str
    last_name: str
    date_of_birth: str
    address: str
    job_title: str
    phone: str


@dataclass
class UserRegistration(UserData):
    """User Registration."""

    password1: str
    password2: str


class UserRegistrationFactory(DataclassFactory[User]):
    """User Registration Factory."""

    __model__ = UserRegistration
    _faker = Field(Locale.RU)

    @classmethod
    def email(cls) -> str:
        """Email override."""
        return cls._faker('email')

    @classmethod
    def date_of_birth(cls) -> str:
        """Date of birth override."""
        return cls._faker('date')


@pytest.fixture()
def user_registration_data(mimesis_field) -> UserRegistration:
    """User Registration Fixture."""
    pw = mimesis_field('password')
    return UserRegistrationFactory.build(
        password1=pw,
        password2=pw,
    )
