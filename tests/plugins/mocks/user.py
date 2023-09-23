from mimesis import Field, Locale
import pytest
from django_fakery.faker_factory import Factory
from faker import Faker


from server.apps.identity.models import User

from dataclasses import dataclass

from polyfactory.factories import DataclassFactory



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
class UserData:
    email: str
    first_name: str
    last_name: str
    date_of_birth: str
    address: str
    job_title: str
    phone: str


@dataclass
class UserRegistration(UserData):
    password1: str
    password2: str


class UserRegistrationFactory(DataclassFactory[User]):
    __model__ = UserRegistration
    _faker = Field(Locale.RU)

    @classmethod
    def email(cls) -> str:
        return cls._faker('email')

    @classmethod
    def date_of_birth(cls) -> str:
        return cls._faker('date')


@pytest.fixture()
def user_registration_data(mimesis_field) -> UserRegistration:
    pw = mimesis_field('password')
    return UserRegistrationFactory.build(
        password1=pw,
        password2=pw,
    )
