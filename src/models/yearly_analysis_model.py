from pymongo import ASCENDING

class YearlyWeatherStatsModel:
    def __init__(self, db):
        self.db = db
        self.collection = db["yearly_weather_stats"]

        # Ensure compound index for fast lookups
        self.collection.create_index([
            ("year", ASCENDING),
            ("station_id", ASCENDING)
        ], unique=True)

    def add_or_update_yearly_stats(self, year, station_id, avg_max_temp, avg_min_temp, total_precipitation):
        """
        Adds or updates the yearly weather statistics for a given year and station.
        :param year: The year for the statistics.
        :param station_id: The weather station ID.
        :param avg_max_temp: Average max temperature in Celsius.
        :param avg_min_temp: Average min temperature in Celsius.
        :param total_precipitation: Total precipitation in centimeters.
        :return: The result of the upsert operation.
        """
        record = {
            "year": year,
            "station_id": station_id,
            "avg_max_temp": avg_max_temp,
            "avg_min_temp": avg_min_temp,
            "total_precipitation": total_precipitation,
        }

        return self.collection.update_one(
            {"year": year, "station_id": station_id},
            {"$set": record},
            upsert=True
        )
