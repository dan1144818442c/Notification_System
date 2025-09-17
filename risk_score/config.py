import os
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "cars_db")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "inserted_collection")