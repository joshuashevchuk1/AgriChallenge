from pymongo import MongoClient, ASCENDING
import os


def initialize_db():
    """
    Initializes and returns a MongoDB client connection.
    Ensures that the 'wx' collection exists and has a compound index on the specified fields.
    """
    client = MongoClient(
        host=os.getenv("MONGO_HOST", "localhost"),
        port=int(os.getenv("MONGO_PORT", 27017)),
        username=os.getenv("MONGO_USER", None),
        password=os.getenv("MONGO_PASS", None),
    )

    db_name = os.getenv("MONGO_DB_NAME", "weather_data")
    db = client[db_name]
    collection = db["wx"]

    # Create a compound index on 'timestamp', 'max_temp', 'min_temp', 'precipitation'
    collection.create_index(
        [("timestamp", ASCENDING),
         ("max_temp", ASCENDING),
         ("min_temp", ASCENDING),
         ("precipitation", ASCENDING)],
        unique=False  # Ensures that the index is not unique, allowing upserts with same timestamp
    )

    return db  # Return the database instance
