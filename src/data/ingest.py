import logging
import os
from datetime import datetime
from models.wx_model import WxModel

class WeatherIngestor:
    def __init__(self, db):
        self.wx_model = WxModel(db)

    @staticmethod
    def get_records(file_path):
        """
        Helper method to get records from a wx txt file
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

    def ingestAll(self, dir):
        """
        Ingests all valid wx txt files in the given directory into the mongo database
        :param dir: directory containing the .txt files
        :return: total count of inserted records
        """
        total_inserted = 0
        logging.info(f"Starting ingestion of all files in directory: {dir}")
        start_time = datetime.now()

        # Check if directory exists
        if not os.path.exists(dir):
            logging.error(f"Directory {dir} does not exist.")
            return 0

        # Get all .txt files in the directory
        txt_files = [f for f in os.listdir(dir) if f.endswith(".txt")]

        if not txt_files:
            logging.warning(f"No .txt files found in directory {dir}.")
            return 0

        for file_name in txt_files:
            file_path = os.path.join(dir, file_name)
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
        Ingests all records in a wx txt file into mongo
        :param file_path:
        :return:
        """

        logging.info("Starting ingestion process")
        start_time = datetime.now()

        records = self.get_records(file_path)
        if not records:
            logging.info("No valid records found. Aborting ingestion.")
            return 0

        # Directly use the insert_many function to bulk insert all records without filtering by timestamp
        inserted_count = self._bulk_insert(records)

        end_time = datetime.now()
        logging.info(f"Finished ingestion process: Inserted {inserted_count} new records for {file_path}")
        logging.info(f"Ingestion duration: {end_time - start_time}")

        return inserted_count

    def _bulk_insert(self, records):
        """
        Bulk inserts all records into the mongo database
        :param records:
        :return:
        """
        # Insert all records using insert_many in WxModel
        inserted_count = self.wx_model.insert_many(records)

        return inserted_count
