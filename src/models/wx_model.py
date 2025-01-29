class WxModel:
    def __init__(self, db):
        self.collection = db["wx"]

    def add_weather_data(self, timestamp, max_temp, min_temp, precipitation):
        try:
            document = {
                "timestamp": timestamp,
                "max_temp": max_temp,
                "min_temp": min_temp,
                "precipitation": precipitation,
            }
            result = self.collection.update_one(
                {"timestamp": timestamp},  # Query to check if it exists
                {"$setOnInsert": document},  # Insert only if missing
                upsert=True  # Ensures insertion but no overwrite
            )
            if result.upserted_id:
                return f"Data inserted with ID: {result.upserted_id}"
            return "Duplicate record skipped"
        except Exception as e:
            return f"Error: {str(e)}"

    def get_weather_data(self, timestamp):
        return self.collection.find_one({"timestamp": timestamp})
