from flask import Flask, jsonify
from flask_restx import Resource, Api

import data.db as db
import logging
from api.weather_handler import WeatherHandler
from data.ingest import WeatherIngestor


class CommonApp:
    def __init__(self, port):
        self.port = port
        self.app = Flask(__name__)
        self.api = Api(
            self.app,
            title='Weather api',
            version='1.0',
            description='AgriChallenge')
        self.weather_ingestor = None
        self.initialize_database()

    def initialize_database(self):
        self.db = db.initialize_db()  # Initialize MongoDB connection
        self.weather_ingestor = WeatherIngestor(self.db)
        logging.info("db and wx_model initialized")

    def ingest(self):
        self.weather_ingestor.ingestAll("./data/wx_data")
        self.weather_ingestor.ingest_aggregates()

    def init_api(self):
        # Initialize the WeatherHandler class
        self.weather_handler = WeatherHandler(self.app, self.db)
        self.weather_handler.add_routes()

    def home(self):
        return "ok", 200

    def health_check(self):
        return "healthcheck", 200

    def add_routes(self):
        logging.info("registering /")

        @self.api.route('/')
        class Home(Resource):
            def get(self):
                """
                Home route
                """
                return {"message": "ok"}

        logging.info("registering /healthcheck")

        @self.api.route('/healthCheck')
        class HealthCheck(Resource):
            def get(self):
                """
                Health check route
                """
                return {"message": "healthcheck"}

    def run_server(self):
        self.add_routes()
        self.app.run("0.0.0.0", self.port, debug=False)
