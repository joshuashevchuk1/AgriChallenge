from pymongo import MongoClient, ASCENDING

from app import config


def initialize_db():
    """
    Initializes and returns a MongoDB client connection.
    Ensures that the 'wx' collection exists and has a compound index on the specified fields.
    """
    client = MongoClient(
        host=config.MONGO_HOST,
        port=int(config.MONGO_PORT),
        username=config.MONGO_USER,
        password=config.MONGO_PASS,
    )

    db_name = config.MONGO_DB_NAME
    db = client[db_name]
    collection = db["wx"]

    # Create a compound index on 'timestamp', 'max_temp', 'min_temp', 'precipitation'
    collection.create_index(
        [("timestamp", ASCENDING),
         ("max_temp", ASCENDING),
         ("min_temp", ASCENDING),
         ("precipitation", ASCENDING),
         ("station_name",ASCENDING)],
        unique=False  # Ensures that the index is not unique, allowing upserts with same timestamp
    )

    return db  # Return the database instance
