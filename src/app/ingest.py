import logging
from datetime import datetime
from models.wx_model import WxModel

class WeatherIngestor:
    def __init__(self, db):
        self.wx_model = WxModel(db)

    @staticmethod
    def _read_file(file_path):
        records = []
        try:
            with open(file_path, "r") as file:
                for line in file:
                    parts = line.strip().split("\t")  # Split by tab character
                    if len(parts) != 4:
                        logging.warning(f"Skipping malformed line: {line.strip()}")
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

    def _insert(self,records):
        inserted_count = 0
        for record in records:
            if self.wx_model.get_weather_data(record["timestamp"]):
                logging.info(f"Skipping duplicate record for timestamp {record['timestamp']}")
                continue  # Skip duplicates

            result = self.wx_model.add_weather_data(
                timestamp=record["timestamp"],
                min_temp=record["min_temp"],
                max_temp=record["max_temp"],
                precipitation=record["precipitation"],
            )
            if "Data inserted" in result:
                inserted_count += 1
        return inserted_count

    def ingest(self, file_path):
        logging.info("Starting ingestion process")
        start_time = datetime.now()

        records = self._read_file(file_path)
        if not records:
            logging.info("No valid records found. Aborting ingestion.")
            return 0

        inserted_count = 0
        self._insert(records)

        end_time = datetime.now()
        logging.info(f"Finished ingestion process: Inserted {inserted_count} new records.")
        logging.info(f"Ingestion duration: {end_time - start_time}")

        return inserted_count
