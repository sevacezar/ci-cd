from datetime import datetime

from flask import Flask, jsonify, request

# from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError

from .database import db
from .models import Client, ClientParking, Parking
from .schemas import ClientParkingSchema, ClientSchema, ParkingSchema
from .services import (
    get_all_clients_db,
    get_client_by_id_db,
    get_client_parking_by_ids_db,
    get_parking_by_id_db,
)

# db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///parking.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    @app.before_first_request
    def create_all_tables():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/clients", methods=["GET"])
    def get_all_clients():
        """Вывод списка всех клиентов"""
        clients = get_all_clients_db()
        return jsonify([i_client.to_json() for i_client in clients]), 200

    @app.route("/clients/<int:client_id>", methods=["GET"])
    def get_client_by_id(client_id: int):
        """Вывод информации о клиенте по его id"""
        client = get_client_by_id_db(client_id)
        if client:
            return client.to_json(), 200
        else:
            return jsonify({"error": "Client's id is not exist"}), 400

    @app.route("/clients", methods=["POST"])
    def add_new_client():
        """Добавление в БД нового клиента"""
        client_schema = ClientSchema()
        try:
            new_client_dict = client_schema.load(request.json)
            new_client = Client(**new_client_dict)
            db.session.add(new_client)
            db.session.commit()
            return jsonify(new_client.to_json()), 201
        except ValidationError as exc:
            return jsonify(validation_error=exc.messages), 400

        """
        curl -H "Content-Type: application/json"
        -X POST
        -d '{"name": "Andrey",
        "surname": "Antonov",
        "credit_card": "XXXXXX",
        "car_number": "K905EO72S"}'
        http://127.0.0.1:5000/clients
        """

    @app.route("/parkings", methods=["POST"])
    def add_new_parking():
        """Добавление в БД новой парковочной зоны"""
        parking_schema = ParkingSchema()
        try:
            new_parking_dict = parking_schema.load(request.json)
            new_parking = Parking(**new_parking_dict)
            db.session.add(new_parking)
            db.session.commit()
            return jsonify(new_parking.to_json()), 201
        except ValidationError as exc:
            return jsonify(validation_error=exc.messages), 400

        """
          curl -X POST -H "Content-Type: application/json"
          -d '{"address": "Respubliki 8",
          "opened": true,
          "count_places": 10,
          "count_available_places": 10}'
          http://127.0.0.1:5000/parkings
        """

    @app.route("/client_parkings", methods=["POST"])
    def add_new_client_parking():
        """Запись в БД заезда на парковку"""
        client_parking_schema = ClientParkingSchema()
        try:
            new_client_parking_dict = client_parking_schema.load(request.json)
            client = get_client_by_id_db(client_id=new_client_parking_dict["client_id"])
            parking = get_parking_by_id_db(
                parking_id=new_client_parking_dict["parking_id"]
            )

            if not client:
                return jsonify(error="Client does not exist"), 400
            if not parking:
                return jsonify(error="Parking does not exist"), 400

            if parking.opened is False:
                return jsonify(message="Parking is closed"), 400
            if parking.count_available_places == 0:
                return jsonify(message="No free places for your car"), 400

            new_client_parking = ClientParking(**new_client_parking_dict)
            new_client_parking.time_in = datetime.now()
            parking.count_available_places -= 1
            db.session.add(new_client_parking)
            db.session.commit()
            return jsonify(new_client_parking.to_json()), 201
        except ValidationError as exc:
            return jsonify(validation_error=exc.messages), 400

        """
          curl -X POST -H "Content-Type: application/json"
          -d '{"client_id": 1,
          "parking_id": 1}'
          http://127.0.0.1:5000/client_parkings
        """

    @app.route("/client_parkings", methods=["DELETE"])
    def delete_client_parking():
        """Фиксация в БД выезда автомобиля с парковки"""
        client_parking_schema = ClientParkingSchema()
        try:
            new_client_parking_dict = client_parking_schema.load(request.json)
            new_client_parking = get_client_parking_by_ids_db(**new_client_parking_dict)
            if not new_client_parking:
                return jsonify(error="No entry"), 400

            if new_client_parking.time_out:
                return (
                    jsonify(error="There is no longer this car in the parking lot"),
                    400,
                )

            if not new_client_parking.client.credit_card:
                return jsonify(message="No credit card linked"), 400

            new_client_parking.time_out = datetime.now()
            new_client_parking.parking.count_available_places += 1
            db.session.commit()
            return jsonify(new_client_parking.to_json()), 201
        except ValidationError as exc:
            return jsonify(validation_error=exc.messages), 400

        """
                  curl -X DELETE -H "Content-Type: application/json"
                  -d '{"client_id": 1,
                  "parking_id": 1}'
                  http://127.0.0.1:5000/client_parkings
        """

    return app
