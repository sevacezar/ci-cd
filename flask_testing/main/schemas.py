from marshmallow import fields, validate, ValidationError, validates
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from .models import Client, Parking, ClientParking



class ClientSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Client

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(max=50))
    surname = fields.Str(required=True, validate=validate.Length(max=50))
    credit_card = fields.Str(validate=validate.Length(max=50))
    car_number = fields.Str(validate=validate.Length(max=10))


class ParkingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Parking

    id = fields.Int(dump_only=True)
    address = fields.Str(required=True, validate=validate.Length(max=100))
    opened = fields.Boolean()
    count_places = fields.Int(required=True)
    count_available_places = fields.Int(required=True)


class ClientParkingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ClientParking

    id = fields.Int(dump_only=True)
    client_id = fields.Int(required=True)
    parking_id = fields.Int(required=True)