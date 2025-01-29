from collections import defaultdict
from datetime import datetime

from models.wx_model import WxModel
from models.yearly_analysis_model import YearlyWeatherStatsModel


class WeatherAnalysis:
    def __init__(self, db):
        self.wx_model = WxModel(db)
        self.yearly_stats_model = YearlyWeatherStatsModel(db)

    def calculate_yearly_stats(self):
        """
        Calculate yearly statistics for each weather station and store them in the database.
        """
        # Fetch all wx records
        records = self.wx_model.get_all_weather_data()

        # Aggregate data by year and station_id
        aggregated_data = defaultdict(lambda: defaultdict(list))

        for record in records:
            try:
                # Extract year and station_id
                year = datetime.strptime(record["timestamp"], "%Y%m%d").year
                station_id = record["station_id"]

                # Only consider valid records
                if None not in [record["max_temp"], record["min_temp"], record["precipitation"]]:
                    aggregated_data[year][station_id].append(record)

            except Exception as e:
                logging.warning(f"Skipping invalid record: {e}")

        # Calculate and insert stats for each year and station
        for year, stations in aggregated_data.items():
            for station_id, records in stations.items():
                max_temps = [r["max_temp"] for r in records]
                min_temps = [r["min_temp"] for r in records]
                precipitations = [r["precipitation"] for r in records]

                avg_max_temp = sum(max_temps) / len(max_temps) if max_temps else None
                avg_min_temp = sum(min_temps) / len(min_temps) if min_temps else None
                total_precipitation = sum(precipitations) / 10.0 if precipitations else None  # Convert to cm

                # Insert or update the stats in the database
                self.yearly_stats_model.add_or_update_yearly_stats(year, station_id, avg_max_temp, avg_min_temp, total_precipitation)

        logging.info("Yearly statistics calculation completed successfully.")
