from datetime import datetime

from flask import Flask
import data.db as db
import logging
from ingest import WeatherIngestor

class CommonApp:
    def __init__(self, port):
        self.port = port
        self.app = Flask(__name__)
        self.weather_ingestor = None
        self._initialize_database()

    def _initialize_database(self):
        self.db = db.initialize_db()  # Initialize MongoDB connection
        self.weather_ingestor = WeatherIngestor(db)
        logging.info("db and wx_model initialized")

    def read_file(self, file_path):
        """
        Reads a weather data file line by line and returns a list of parsed records.
        """
        records = []
        try:
            with open(file_path, "r") as file:
                for line in file:
                    parts = line.strip().split("\t")  # Split by tab
                    if len(parts) != 4:
                        logging.warning(f"Skipping malformed line: {line}")
                        continue

                    timestamp, min_temp, max_temp, precipitation = parts
                    records.append({
                        "timestamp": timestamp,
                        "min_temp": float(min_temp),
                        "max_temp": float(max_temp),
                        "precipitation": float(precipitation),
                    })
        except Exception as e:
            logging.error(f"Error reading file {file_path}: {e}")

        return records

    def ingest(self):
        self.weather_ingestor

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
        self.app.run("0.0.0.0", self.port, debug=True)
