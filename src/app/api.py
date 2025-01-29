from flask import Flask, request
from flask_restx import Resource, Api

import app.data.db as db
import logging
from app.data.ingest import WeatherIngestor
from app.models.weather_aggregates import WeatherAggregatesModel
from app.models.weather_records import WeatherRecordsModel


class WeatherApi:
    def __init__(self, port):
        self.db = None
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
        self.weather_ingestor.ingestAll("./app/data/wx_data")
        self.weather_ingestor.ingest_aggregates()

    @staticmethod
    def home():
        return "ok", 200

    @staticmethod
    def health_check():
        return "healthcheck", 200

    def add_routes(self, param_db):
        logging.info("registering /")

        weather_records_model = WeatherRecordsModel(param_db)
        weather_aggregates_model = WeatherAggregatesModel(param_db)

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

        @self.api.route('/api/weather')
        class WeatherResource(Resource):
            def get(self):
                """
                Get weather data based on filter parameters.
                Can filter by station_name, date, and apply pagination.
                """
                filter_criteria = {}
                date = request.args.get("date")
                station_name = request.args.get("station_name")
                skip = int(request.args.get("skip", 0))
                limit = int(request.args.get("limit", 100))

                if date:
                    filter_criteria["date"] = date
                if station_name:
                    filter_criteria["station_name"] = station_name

                weather_data = weather_records_model.get_weather_data(filter_criteria, skip, limit)
                return {"weather_data": weather_data}, 200

        @self.api.route('/api/weather/stats')
        class WeatherStatsResource(Resource):
            def get(self):
                """
                Get weather aggregate statistics based on filter parameters.
                Can filter by station_name, year, and apply pagination.
                """
                filter_criteria = {}
                station_name = request.args.get("station_name")
                year = request.args.get("year")
                skip = int(request.args.get("skip", 0))
                limit = int(request.args.get("limit", 100))

                if station_name:
                    filter_criteria["station_name"] = station_name
                if year:
                    filter_criteria["year"] = int(year)  # Ensure year is an integer

                print(f"Filter criteria for weather stats: {filter_criteria}")

                weather_aggregates = weather_aggregates_model.get_weather_data(filter_criteria, skip, limit)

                if not weather_aggregates:
                    return {"error": "No data found"}, 404

                return {"weather_aggregates": weather_aggregates}, 200

    def run_server(self):
        self.add_routes(self.db)
        self.app.run("0.0.0.0", self.port, debug=False)
