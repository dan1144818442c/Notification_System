import os


KAFKA_BROKERS = os.getenv("KAFKA_BROKERS", "localhost:9092")
KAFKA_PERSISTER_GROUP_ID = os.getenv("KAFKA_PERSISTER_GROUP_ID", "persister_group")
KAFKA_PERSISTER_TOPIC = os.getenv("KAFKA_PERSISTER_TOPIC",'cars_with_details')
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "cars_db")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "inserted_collection")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "100"))