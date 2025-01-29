from pymongo import UpdateOne

class WxModel:
    def __init__(self, db):
        self.db = db
        self.collection = db["wx"]

    def insert_many(self, records, batch_size=1000):
        """
        Performs a bulk upsert of records into the database in batches.
        :param records: List of records to insert or update
        :param batch_size: The batch size for the bulk operation
        :return: The number of records successfully upserted
        """
        operations = []
        total_upserted = 0

        # Iterate over records in batches
        for i, record in enumerate(records):
            operations.append(
                UpdateOne(
                    {"timestamp": record["timestamp"],
                     "max_temp": record["max_temp"],
                     "min_temp": record["min_temp"],
                     "precipitation": record["precipitation"],
                     "station_name": record["station_name"]},
                    {
                        "$set": {
                            "timestamp": record["timestamp"],
                            "max_temp": record["max_temp"],
                            "min_temp": record["min_temp"],
                            "precipitation": record["precipitation"],
                            "station_name": record["station_name"]
                        }
                    },
                    upsert=True
                )
            )

            # If batch size is reached, execute the bulk_write operation
            if len(operations) >= batch_size:
                result = self.collection.bulk_write(operations)
                total_upserted += result.upserted_count + result.modified_count
                operations.clear()  # Clear operations for the next batch

        # If there are any remaining operations after the loop, execute them
        if operations:
            result = self.collection.bulk_write(operations)
            total_upserted += result.upserted_count + result.modified_count

        return total_upserted

    def get_all_weather_data(self):
        pass
