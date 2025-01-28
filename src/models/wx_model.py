class WxModel:
    def __init__(self, db):
        self.collection = db.wx  # The `wx` collection in the database

    def add_weather_data(self, timestamp, max_temp, min_temp, precipitation):
        try:
            document = {
                "timestamp": timestamp,
                "max_temp": max_temp,
                "min_temp": min_temp,
                "precipitation": precipitation,
            }
            result = self.collection.insert_one(document)
            return f"Data inserted with ID: {result.inserted_id}"
        except Exception as e:
            return f"Error: {str(e)}"

    def get_weather_data(self, timestamp):
        return self.collection.find_one({"timestamp": timestamp})
