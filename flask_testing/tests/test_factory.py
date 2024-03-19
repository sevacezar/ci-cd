from flask_testing.main.models import Client, ClientParking, Parking
from flask_testing.main.services import get_all_clients_db, get_all_parkings_db

from .factories import ClientFactory, ParkingFactory


def test_create_client(client, app, db):
    clients_count = len(get_all_clients_db())
    new_client = ClientFactory()
    db.session.commit()
    assert len(get_all_clients_db()) - clients_count == 1
    assert new_client.id == 2


def test_create_parking(client, app, db):
    parking_count = len(get_all_parkings_db())
    new_parking = ParkingFactory()
    db.session.commit()
    assert len(get_all_parkings_db()) - parking_count == 1
    assert new_parking.id == 2
