import logging
from datetime import datetime
from models.wx_model import WxModel
import concurrent.futures

class WeatherIngestor:
    def __init__(self, db):
        self.wx_model = WxModel(db)

    @staticmethod
    def get_records(file_path):
        """
        helper method to get records from a wx txt file
        :param file_path:
        :return:
        """
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

    def _bulk_insert(self, records):
        """
        bulk inserts all records into the mongo database
        :param records:
        :return:
        """
        existing_timestamps = set(self.wx_model.get_existing_timestamps())  # Load all existing timestamps in bulk

        records_to_insert = [record for record in records if record["timestamp"] not in existing_timestamps]

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self._insert_record, records_to_insert)

            # Count how many inserts were successful
            inserted_count = sum(1 for result in results if "Data inserted" in result)

        return inserted_count

    def _insert_record(self, record):
        """
        calls the add weather data method on the wx_model to insert the record into the mongo database
        :param record:
        :return:
        """

        result = self.wx_model.add_weather_data(
            timestamp=record["timestamp"],
            min_temp=record["min_temp"],
            max_temp=record["max_temp"],
            precipitation=record["precipitation"],
        )
        return result

    def ingest(self, file_path):
        """
        ingests all records in a wx txt file into mongo
        :param file_path:
        :return:
        """

        logging.info("Starting ingestion process")
        start_time = datetime.now()

        records = self.get_records(file_path)
        if not records:
            logging.info("No valid records found. Aborting ingestion.")
            return 0

        inserted_count = self._bulk_insert(records)

        end_time = datetime.now()
        logging.info(f"Finished ingestion process: Inserted {inserted_count} new records for {file_path}")
        logging.info(f"Ingestion duration: {end_time - start_time}")

        return inserted_count
