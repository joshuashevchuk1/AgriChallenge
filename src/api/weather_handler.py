from flask import request, jsonify
from flasgger import Swagger, swag_from
from src.models.weather_records import WeatherRecordsModel
from src.models.weather_aggregates import WeatherAggregatesModel

class WeatherHandler:
    def __init__(self, app, db):
        self.app = app
        self.weather_records_model = WeatherRecordsModel(db)
        self.weather_aggregates_model = WeatherAggregatesModel(db)
        Swagger(app)  # Initialize Flasgger for auto-generation of Swagger documentation

    def get_weather(self):
        """
        Endpoint to get weather data based on filter parameters.
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

        weather_data = self.weather_records_model.get_weather_data(filter_criteria, skip, limit)
        return jsonify({"weather_data": weather_data}), 200

    def get_weather_stats(self):
        """
        Endpoint to get weather aggregate statistics based on filter parameters.
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

        # Log the filter criteria
        print(f"Filter criteria for weather stats: {filter_criteria}")

        weather_aggregates = self.weather_aggregates_model.get_weather_data(filter_criteria, skip, limit)

        if not weather_aggregates:
            return jsonify({"error": "No data found"}), 404

        return jsonify({"weather_aggregates": weather_aggregates}), 200

    def add_routes(self):
        """
        Add routes for the weather data and aggregate statistics.
        """
        self.app.add_url_rule('/api/weather', 'get_weather', self.get_weather, methods=["GET"])
        self.app.add_url_rule('/api/weather/stats', 'get_weather_stats', self.get_weather_stats, methods=["GET"])

