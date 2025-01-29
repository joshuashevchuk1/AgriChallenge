from pymongo import UpdateOne

class WeatherAggregatesModel:
    def __init__(self, db):
        self.db = db
        self.wx_collection = db["wx"]
        self.aggregate_collection = db["weather_aggregates"]

    def aggregate_and_insert(self, batch_size=1000):
        """
        Aggregates weather data from the wx collection and inserts the aggregated results into the weather_aggregates collection.
        :param batch_size: The batch size for the bulk operation
        :return: The number of records successfully upserted
        """
        operations = []
        total_upserted = 0

        # Aggregation pipeline to compute the required statistics
        pipeline = [
            # Match stage to filter out null values and -9999 values
            {
                "$match": {
                    "max_temp": {"$ne": None, "$ne": -9999},
                    "min_temp": {"$ne": None, "$ne": -9999},
                    "precipitation": {"$ne": None, "$ne": -9999}
                }
            },
            {
                "$project": {
                    "station_name": 1,
                    "year": {
                        "$year": {
                            "$toDate": {
                                "$concat": [
                                    {"$substr": [{"$toString": "$timestamp"}, 0, 4]},  # Year (first 4 digits)
                                    "-",
                                    {"$substr": [{"$toString": "$timestamp"}, 4, 2]},  # Month (next 2 digits)
                                    "-",
                                    {"$substr": [{"$toString": "$timestamp"}, 6, 2]}  # Day (last 2 digits)
                                ]
                            }
                        }
                    },
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
                    "avg_max_temp": {
                        "$cond": {
                            "if": {"$gt": ["$count", 0]},
                            "then": {"$divide": ["$max_temp_sum", "$count"]},
                            "else": None
                        }
                    },
                    "avg_min_temp": {
                        "$cond": {
                            "if": {"$gt": ["$count", 0]},
                            "then": {"$divide": ["$min_temp_sum", "$count"]},
                            "else": None
                        }
                    },
                    "total_precipitation": {
                        "$cond": {
                            "if": {"$gt": ["$count", 0]},
                            "then": {"$divide": ["$precipitation_sum", 10]},  # Convert to cm
                            "else": None
                        }
                    }
                }
            }
        ]

        # Run the aggregation pipeline
        aggregated_results = self.wx_collection.aggregate(pipeline)

        # Prepare the upsert operations for the weather_aggregates collection
        for result in aggregated_results:
            operations.append(
                UpdateOne(
                    {"station_name": result["station_name"], "year": result["year"]},
                    {
                        "$set": {
                            "avg_max_temp": result["avg_max_temp"],
                            "avg_min_temp": result["avg_min_temp"],
                            "total_precipitation": result["total_precipitation"]
                        }
                    },
                    upsert=True
                )
            )

            # If batch size is reached, execute the bulk_write operation
            if len(operations) >= batch_size:
                result = self.aggregate_collection.bulk_write(operations)
                total_upserted += result.upserted_count + result.modified_count
                operations.clear()  # Clear operations for the next batch

        # Final bulk write for any remaining operations
        if operations:
            result = self.aggregate_collection.bulk_write(operations)
            total_upserted += result.upserted_count + result.modified_count

        return total_upserted