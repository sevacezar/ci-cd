from sqlalchemy.ext.associationproxy import association_proxy

from .app import db


class Client(db.Model):  # type: ignore
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))

    parking_associations = db.relationship("ClientParking", back_populates="client")
    parkings = association_proxy("parking_associations", "parking")

    def __repr__(self):
        return f"<Client {self.name} {self.surname}>"

    def to_json(self):
        return {item.name: getattr(self, item.name) for item in self.__table__.columns}


class Parking(db.Model):  # type: ignore
    __tablename__ = "parkings"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    client_associations = db.relationship("ClientParking", back_populates="parking")
    clients = association_proxy("client_associations", "client")

    def __repr__(self):
        return f"<Parking on {self.address}>"

    def to_json(self):
        return {item.name: getattr(self, item.name) for item in self.__table__.columns}


class ClientParking(db.Model):  # type: ignore
    __tablename__ = "client_parkings"

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id"))
    parking_id = db.Column(db.Integer, db.ForeignKey("parkings.id"))
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)

    client = db.relationship("Client", back_populates="parking_associations")
    parking = db.relationship("Parking", back_populates="client_associations")

    def __repr__(self):
        return f"<ClientParking {self.id}>"

    def to_json(self):
        return {item.name: getattr(self, item.name) for item in self.__table__.columns}
