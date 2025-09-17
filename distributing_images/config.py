import os

MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "car_pictures")
ID_TOPIC = os.getenv("ID_TOPIC", "id_topic")