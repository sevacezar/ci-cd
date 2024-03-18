from .models import db, Client, ClientParking, Parking

from typing import List, Optional


def get_all_clients_db() -> List[Client]:
    return db.session.query(Client).all()


def get_all_parkings_db() -> List[Parking]:
    return db.session.query(Parking).all()


def get_client_by_id_db(client_id: int) -> Optional[Client]:
    return db.session.query(Client).filter_by(id=client_id).one_or_none()


def get_parking_by_id_db(parking_id: int) -> Optional[Parking]:
    return db.session.query(Parking).filter_by(id=parking_id).one_or_none()


def get_client_parking_by_ids_db(client_id: int, parking_id: int) -> Optional[ClientParking]:
    return db.session.query(ClientParking).filter_by(client_id=client_id, parking_id=parking_id).one_or_none()
