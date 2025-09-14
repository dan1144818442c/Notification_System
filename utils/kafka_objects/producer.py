from kafka import KafkaProducer
import json
from log.logger import Logger

logger = Logger.get_logger("Producer_logger")

class Producer:
    """Kafka Producer"""
    def __init__(self,bootstrap_servers= 'localhost:9092',
                 encode = 'utf-8'):
        self.producer = KafkaProducer(bootstrap_servers=[bootstrap_servers],
                             value_serializer=lambda x:
                             json.dumps(x, default=str).encode(encode))

    def publish_message(self,topic,message):
        """Publish a message to a Kafka topic."""
        self.producer.send(topic, message)
        self.producer.flush()
        logger.info(f"Message published to topic '{topic}'.")