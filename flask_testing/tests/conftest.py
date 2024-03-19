from datetime import datetime, timedelta

import pytest

from flask_testing.main.app import create_app
from flask_testing.main.app import db as _db
from flask_testing.main.models import Client, ClientParking, Parking


# @pytest.fixture
@pytest.fixture(scope="module")  # чтобы в БД копились записи от теста к тесту
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"

    with _app.app_context():
        _db.create_all()
        client = Client(
            name="name",
            surname="surname",
            credit_card="credit_card",
            car_number="car_number",
        )
        parking = Parking(
            address="address", opened=True, count_places=10, count_available_places=10
        )
        time_in = datetime.now()
        time_out = time_in + timedelta(hours=2)
        client_parking = ClientParking(time_in=time_in, time_out=time_out)
        client_parking.client = client
        client_parking.parking = parking
        _db.session.add_all([client_parking, client, parking])
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db
