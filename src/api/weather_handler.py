from flask import request, jsonify
from src.models.weather_records import WeatherRecordsModel # Assuming you have a weather data model
from src.models.weather_aggregates import WeatherAggregatesModel  # Assuming you have the weather aggregates model
from flask_swagger_ui import get_swaggerui_blueprint

class WeatherHandler:
    def __init__(self, app):
        self.app = app
        self.weather_model = WeatherRecordsModel(self.app.db)  # Instance of your weather model
        self.weather_aggregates_model = WeatherAggregatesModel(self.app.db)  # Instance of your weather aggregates model

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

        weather_data = self.weather_model.get_weather_data(filter_criteria, skip, limit)
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
            filter_criteria["year"] = year

        weather_aggregates = self.weather_aggregates_model.get_weather_data(filter_criteria, skip, limit)
        return jsonify({"weather_aggregates": weather_aggregates}), 200

    def add_routes(self):
        """
        Add routes for the weather data and aggregate statistics.
        """
        self.app.add_url_rule('/api/weather', 'get_weather', self.get_weather, methods=["GET"])
        self.app.add_url_rule('/api/weather/stats', 'get_weather_stats', self.get_weather_stats, methods=["GET"])

    def init_swagger(self):
        """
        Initialize Swagger UI for API documentation.
        """
        swagger_url = '/swagger'
        api_url = '/static/swagger.json'  # Path to your Swagger JSON
        swagger_ui_blueprint = get_swaggerui_blueprint(
            swagger_url,
            api_url,
            config={'app_name': "Weather API"}
        )
        self.app.register_blueprint(swagger_ui_blueprint, url_prefix=swagger_url)
