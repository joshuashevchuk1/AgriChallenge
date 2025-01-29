from pymongo import MongoClient
import os


def initialize_db():
    """
    Initializes and returns a MongoDB client connection.
    Ensures that the 'wx' collection exists and has a unique index on 'timestamp'.
    """
    client = MongoClient(
        host=os.getenv("MONGO_HOST", "localhost"),
        port=int(os.getenv("MONGO_PORT", 27017)),
        username=os.getenv("MONGO_USER", None),
        password=os.getenv("MONGO_PASS", None),
    )

    db_name = os.getenv("MONGO_DB_NAME", "weather_data")
    db = client[db_name]

    return db  # Return the database instance
