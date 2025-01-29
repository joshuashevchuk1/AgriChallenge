from flask import Flask
import data.db as db
import logging
from data.ingest import WeatherIngestor


class CommonApp:
    def __init__(self, port):
        self.port = port
        self.app = Flask(__name__)
        self.weather_ingestor = None
        self._initialize_database()

    def _initialize_database(self):
        self.db = db.initialize_db()  # Initialize MongoDB connection
        self.weather_ingestor = WeatherIngestor(self.db)
        logging.info("db and wx_model initialized")

    def init_app(self):
        self.weather_ingestor.ingest("./data/wx_data.txt")

    def home(self):
        return "ok", 200

    def health_check(self):
        return "healthcheck", 200

    def add_routes(self):
        logging.info("registering /")
        self.app.add_url_rule(
            '/', 'home', self.home, methods=["GET"]
        )
        logging.info("registering /healthcheck")
        self.app.add_url_rule(
            '/healthCheck', 'health_check', self.health_check, methods=["GET"]
        )

    def run_server(self):
        self.add_routes()
        self.app.run("0.0.0.0", self.port, debug=False)
