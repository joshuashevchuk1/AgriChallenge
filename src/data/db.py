from pymongo import MongoClient
import os

# MongoDB connection setup
def initialize_db():
    """
    Initializes and returns a MongoDB client connection.
    """
    client = MongoClient(
        host=os.getenv("MONGO_HOST", "localhost"),
        port=int(os.getenv("MONGO_PORT", 27017)),
        username=os.getenv("MONGO_USER", None),
        password=os.getenv("MONGO_PASS", None),
    )
    db_name = os.getenv("MONGO_DB_NAME", "weather_data")
    return client[db_name]  # Return the database instance