import os

from log.logger import Logger
from retrieve_original_car_details import Retriever
from utils.kafka_objects.consumer import Consumer
from utils.kafka_objects.producer import Producer


class Manager:
    def __init__(self):
        self.in_topic = os.environ.get("IN_TOPIC", "current_details_topic")
        self.out_topic = os.environ.get("OUT_TOPIC", "original_details_topic")
        self.consumer = self.consumer = Consumer(topics=self.in_topic)
        self.producer = Producer()
        self.retriever = Retriever()
        self.logger = Logger.get_logger()


    def process_messages(self) -> None:
        """Process messages from the consumer, enrich them, and publish to the producer."""
        self.logger.info(f"Listening for messages from Kafka topic - {self.in_topic} ...")
        for message in self.consumer.consumer:
            try:
                self.logger.info(f"Received message: {message.value}")
                license_plate = message.value.get("licence_plate")
                type = message.value.get("type")
                message.value["original_details"] = self.retriever.retrieve_cars_data(license_plate, type)

                self.logger.info(f"Publishing processed message - {message.value} to kafka topic '{self.out_topic}'...")
                self.producer.publish_message(self.out_topic, message.value)
                self.consumer.consumer.commit()
                self.logger.info("Processed message sent and committed successfully.")

            except Exception as e:
                self.logger.error(f"Error processing message: {e}")


if __name__ == "__main__":
    manager = Manager()
    manager.process_messages()