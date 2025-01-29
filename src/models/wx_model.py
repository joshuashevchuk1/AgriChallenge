from pymongo import UpdateOne

class WxModel:
    def __init__(self, db):
        self.db = db
        self.collection = db["weather_data"]

    def insert_many(self, records):
        """
        Performs a bulk upsert of records into the database.
        :param records: List of records to insert or update
        :return: The number of records successfully upserted
        """
        operations = []
        for record in records:
            operations.append(
                UpdateOne(
                    {"timestamp": record["timestamp"],
                     "max_temp": record["max_temp"],
                     "min_temp": record["min_temp"],
                     "precipitation": record["precipitation"]},
                    {
                        "$set": {
                            "timestamp": record["timestamp"],
                            "max_temp": record["max_temp"],
                            "min_temp": record["min_temp"],
                            "precipitation": record["precipitation"]
                        }
                    },
                    upsert=True
                )
            )

        if operations:
            result = self.collection.bulk_write(operations)
            return result.upserted_count + result.modified_count  # Return both inserted and modified records count

        return 0  # Return 0 if no operations were performed
