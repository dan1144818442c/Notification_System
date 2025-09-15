from utils.kafka_objects.consumer import Consumer
from utils.mongo_client.connection import Connection
from utils.mongo_client.dal import MongoDAL
from pymongo import MongoClient
from config import *
from log.logger import Logger
from datetime import datetime

logger = Logger.get_logger("Writer_logger")

for message in Consumer(group_id=KAFKA_PERSISTER_GROUP_ID, topics=[KAFKA_PERSISTER_TOPIC]).consumer:
    try:
        logger.info(f"Received message: {message.value}")
        data = {
            "car_id": message.value.get("number"),
            "entry_time": datetime.now()
        }
        mongo_client = MongoClient(MONGO_CONNECTION_STRING)
        mongo_conn = Connection(mongo_client, MONGO_DB_NAME)
        mongo_dal = MongoDAL(mongo_conn)
        mongo_dal.insert_document(MONGO_COLLECTION_NAME, data)
        logger.info("Message inserted into MongoDB successfully.")
    except Exception as e:
        logger.error(f"Error processing message: {e}")

