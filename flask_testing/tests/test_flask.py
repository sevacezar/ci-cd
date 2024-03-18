import pytest

from flask_testing.main.services import (get_all_clients_db,
                                         get_all_parkings_db,
                                         get_parking_by_id_db,
                                         get_client_by_id_db,
                                         get_client_parking_by_ids_db)


@pytest.mark.parametrize('route', ['/clients', '/clients/1'])
def test_route_status(client, route):
    response = client.get(route)
    assert response.status_code == 200


def test_create_client(client, app, db):
    client_data = {"name": "Andrey",
                   "surname": "Antonov",
                   "credit_card": "XXXXXX",
                   "car_number": "K905EO72S"}
    clients_count = len(get_all_clients_db())
    resp = client.post('/clients', json=client_data)
    assert resp.status_code == 201
    assert len(get_all_clients_db()) - clients_count == 1
    assert resp.json['id'] == 2


def test_create_parking(client):
    parking_data = {"address": "Respubliki 8",
                    "opened": True,
                    "count_places": 10,
                    "count_available_places": 10}
    parking_count = len(get_all_parkings_db())
    resp = client.post('/parkings', json=parking_data)
    assert resp.status_code == 201
    assert len(get_all_parkings_db()) - parking_count == 1
    assert resp.json['id'] == 2


@pytest.mark.parking
def test_drive_in(client):
    client_id = 2
    parking_id = 2
    parking_client_data = {"client_id": client_id, "parking_id": parking_id}
    count_available_places = get_parking_by_id_db(parking_id).count_available_places

    resp = client.post('/client_parkings', json=parking_client_data)
    parking = get_parking_by_id_db(parking_id)
    assert resp.status_code == 201
    assert resp.json['id'] == 2
    assert parking.opened
    assert count_available_places - parking.count_available_places == 1


@pytest.mark.parking
def test_drive_out(client):
    client_id = 2
    parking_id = 2
    parking_client_data = {"client_id": client_id, "parking_id": parking_id}
    count_available_places = get_parking_by_id_db(parking_id).count_available_places

    resp = client.delete('/client_parkings', json=parking_client_data)
    parking = get_parking_by_id_db(parking_id)
    client = get_client_by_id_db(client_id)
    client_parking = get_client_parking_by_ids_db(client_id=client_id, parking_id=parking_id)
    assert resp.status_code == 201
    assert parking.count_available_places - count_available_places == 1
    assert client.credit_card
    assert client_parking.time_out > client_parking.time_in

