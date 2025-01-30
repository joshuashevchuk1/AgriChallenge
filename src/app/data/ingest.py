import logging
import os

from datetime import datetime

from app import util
from app.models.weather_aggregates import WeatherAggregatesModel
from app.models.weather_records import WeatherRecordsModel

class WeatherIngestor:
    def __init__(self, db):
        self.wx_model = WeatherRecordsModel(db)
        self.weather_aggregates = WeatherAggregatesModel(db)

    def ingest_all(self, dir_path):
        """
        Ingests all valid wx txt files in the given directory into the mongo database.
        :param dir_path: directory containing the .txt files
        :return: total count of inserted records
        """
        total_inserted = 0
        logging.info(f"Starting ingestion of all files in directory: {dir_path}")
        start_time = datetime.now()

        # Check if directory exists
        if not os.path.exists(dir_path):
            logging.error(f"Directory {dir_path} does not exist.")
            return 0

        # Get all .txt files in the directory
        txt_files = [f for f in os.listdir(dir_path) if f.endswith(".txt")]

        if not txt_files:
            logging.warning(f"No .txt files found in directory {dir_path}.")
            return 0

        for file_name in txt_files:
            file_path = os.path.join(dir_path, file_name)
            logging.info(f"Processing file: {file_path}")

            # Use the existing ingest method for each file
            inserted_count = self.ingest(file_path)
            total_inserted += inserted_count

        end_time = datetime.now()
        logging.info(f"Finished ingestion of all files. Total records inserted: {total_inserted}")
        logging.info(f"Ingestion duration: {end_time - start_time}")

        return total_inserted

    def ingest(self, file_path):
        """
        Ingests all records in a wx txt file into mongo.
        :param file_path: Path to the weather file
        :return: Count of inserted records
        """

        logging.info("Starting ingestion process")
        start_time = datetime.now()

        records = util.get_records(file_path)
        if not records:
            logging.info("No valid records found. Aborting ingestion.")
            return 0

        # Directly use the insert_many function to bulk insert all
        # records without filtering by timestamp
        inserted_count = self._bulk_insert(records)

        end_time = datetime.now()
        logging.info(f"Finished ingestion process: Inserted "
                     f"{inserted_count} new records for {file_path}")
        logging.info(f"Ingestion duration: {end_time - start_time}")

        return inserted_count

    def _bulk_insert(self, records):
        """
        Bulk inserts all records into the mongo database.
        :param records: List of records to insert
        :return: Number of records inserted
        """
        # Insert all records using insert_many in WxModel
        inserted_count = self.wx_model.insert_many(records)

        return inserted_count

    def ingest_aggregates(self, batch_size=1000):
        """
        Ingests aggregated weather data into the weather_aggregates collection by
        calling the aggregate_and_insert method from WeatherAggregatesModel.
        :param batch_size: The batch size for the bulk operation
        :return: The number of records successfully upserted
        """
        total_upserted = self.weather_aggregates.aggregate_and_insert(batch_size)
        print(f"Total records upserted: {total_upserted}")
        return total_upserted