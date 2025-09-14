from kafka import KafkaConsumer
import json
from log.logger import Logger

logger = Logger.get_logger("Consumer_logger")

class Consumer:
    def __init__(self, topics:list[str], bootstrap_server:str ='localhost:9092',
                 decode:str = 'utf-8' ):
        """
        Initializes the Kafka Consumer.
        """
        self.topics = topics
        self._consumer = KafkaConsumer(
            *self.topics,
            group_id='mongo&elastic-group',
            value_deserializer=lambda m: json.loads(m.decode(decode)),
            bootstrap_servers= [bootstrap_server],
            auto_offset_reset='earliest',
            enable_auto_commit=False,
            max_poll_interval_ms=1200000
        )
        logger.info(f"Kafka consumer subscribed to topics '{self.topics}'.")

    @property
    def consumer(self):
        """
        Returns the consumer object
        that holds information messages etc.

        """

        return self._consumer


