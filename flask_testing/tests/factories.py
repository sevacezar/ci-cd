import random
import string

import factory
from factory.faker import Faker
from factory import LazyAttribute

from flask_testing.main.app import db
from flask_testing.main.models import Client, Parking


def _generate_random_text(length: int):
    letters = string.ascii_letters
    return "".join(random.choice(letters) for _ in range(length))


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name: Faker = factory.Faker("first_name")
    surname: Faker = factory.Faker("last_name")
    credit_card: LazyAttribute = factory.LazyAttribute(
        lambda o: random.choice(
            [str(random.randint(1000000000000000, 9999999999999999)), None]
        )
    )
    car_number: LazyAttribute = factory.LazyAttribute(lambda o: _generate_random_text(9))


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address: Faker = factory.Faker("address")
    opened = random.choice([True, False])
    count_places = random.randint(10, 100)
    count_available_places = random.randint(0, count_places)
