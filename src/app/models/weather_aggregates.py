from pymongo import UpdateOne

class WeatherAggregatesModel:
    def __init__(self, db):
        self.db = db
        self.wx_collection = db["wx"]
        self.aggregate_collection = db["weather_aggregates"]

    def get_weather_data(self, filters=None, skip=0, limit=100):
        """
        Fetches weather aggregate data with optional filters and pagination.
        :param filters:
        :param skip:
        :param limit:
        :return:
        """
        filters = filters or {}
        weather_records = list(self.aggregate_collection.find(filters).skip(skip).limit(limit))

        # Convert ObjectId to string for readability
        for record in weather_records:
            record["_id"] = str(record["_id"])

        return weather_records

    def aggregate_and_insert(self, batch_size=1000):
        """
        Aggregates weather data and upserts results into weather_aggregates.
        :param batch_size:
        :return:
        """
        operations = []
        total_updated = 0

        # Aggregate yearly stats for each station
        pipeline = [
            {"$match": {"max_temp": {"$ne": -9999}, "min_temp": {"$ne": -9999}, "precipitation": {"$ne": -9999}}},
            {
                "$project": {
                    "station_name": 1,
                    "year": {"$year": {"$toDate": {"$concat": [
                        {"$substr": [{"$toString": "$timestamp"}, 0, 4]}, "-",
                        {"$substr": [{"$toString": "$timestamp"}, 4, 2]}, "-",
                        {"$substr": [{"$toString": "$timestamp"}, 6, 2]}
                    ]}}},
                    "max_temp": 1,
                    "min_temp": 1,
                    "precipitation": 1,
                }
            },
            {
                "$group": {
                    "_id": {"station_name": "$station_name", "year": "$year"},
                    "max_temp_sum": {"$sum": "$max_temp"},
                    "min_temp_sum": {"$sum": "$min_temp"},
                    "precipitation_sum": {"$sum": "$precipitation"},
                    "count": {"$sum": 1}
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "station_name": "$_id.station_name",
                    "year": "$_id.year",
                    "avg_max_temp": {"$divide": ["$max_temp_sum", "$count"]},
                    "avg_min_temp": {"$divide": ["$min_temp_sum", "$count"]},
                    "total_precipitation": {"$divide": ["$precipitation_sum", 10]}  # Convert mm to cm
                }
            }
        ]

        for result in self.wx_collection.aggregate(pipeline):
            operations.append(
                UpdateOne(
                    {"station_name": result["station_name"], "year": result["year"]},
                    {"$set": {
                        "avg_max_temp": result["avg_max_temp"],
                        "avg_min_temp": result["avg_min_temp"],
                        "total_precipitation": result["total_precipitation"]
                    }},
                    upsert=True
                )
            )

            # Bulk write in batches for efficiency
            if len(operations) >= batch_size:
                res = self.aggregate_collection.bulk_write(operations)
                total_updated += res.upserted_count + res.modified_count
                operations.clear()  # Reset batch

        # Write remaining updates
        if operations:
            res = self.aggregate_collection.bulk_write(operations)
            total_updated += res.upserted_count + res.modified_count

        return total_updated
