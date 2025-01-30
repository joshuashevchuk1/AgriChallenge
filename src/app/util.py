import os
import logging

def get_records(file_path):
    """
    Helper method to get records from a wx txt file.
    The station ID is extracted from the file name and added to each record.
    :param file_path: Path to the weather file
    :return: List of records with station_name included
    """
    records = []
    try:
        # Extract the station_name from the file name (assumes file name is station_name.txt)
        station_name = os.path.basename(file_path).split('.')[0]

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
                    "station_name": station_name,  # Add station_name from file name
                })
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")

    return records