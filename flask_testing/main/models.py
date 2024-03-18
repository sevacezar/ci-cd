from datetime import datetime

from sqlalchemy.ext.associationproxy import association_proxy

from .app import db


class Client(db.Model):
    __tablename__ = 'clients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))

    parking_associations = db.relationship('ClientParking', back_populates='client')
    parkings = association_proxy('parking_associations', 'parking')

    def __repr__(self):
        return f'<Client {self.name} {self.surname}>'

    def to_json(self):
        return {item.name: getattr(self, item.name) for item in self.__table__.columns}


class Parking(db.Model):
    __tablename__ = 'parkings'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places = db.Column(db.Integer, nullable=False)

    client_associations = db.relationship('ClientParking', back_populates='parking')
    clients = association_proxy('client_associations', 'client')

    def __repr__(self):
        return f'<Parking on {self.address}>'

    def to_json(self):
        return {item.name: getattr(self, item.name) for item in self.__table__.columns}


class ClientParking(db.Model):
    __tablename__ = 'client_parkings'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    parking_id = db.Column(db.Integer, db.ForeignKey('parkings.id'))
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)

    client = db.relationship('Client', back_populates='parking_associations')
    parking = db.relationship('Parking', back_populates='client_associations')

    def __repr__(self):
        return f'<ClientParking {self.id}>'

    def to_json(self):
        return {item.name: getattr(self, item.name) for item in self.__table__.columns}


# if __name__ == '__main__':
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///parking.db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     with app.app_context():
#         db.init_app(app)
#         db.create_all()
#         client1 = Client(name='Name', surname='Surname', credit_card='XXX', car_number='E905EO')
#         parking1 = Parking(address='Atrium', opened=True, count_places=10, count_available_places=10)
#         log1 = ClientParking(time_in=datetime.now())
#         log1.client = client1
#         log1.parking = parking1
#         db.session.add(log1)
#         db.session.commit()
