from utils.kafka_objects.consumer import Consumer
from utils.kafka_objects.producer import Producer
from utils.mongo_client.dal import MongoDAL
import json

class RiskScore:
    def __init__(self, topics:list[str], publisher_topic):
        self.topics = topics
        self.consumer = Consumer(topics)
        self.producer = Producer()
        self.publisher_topic = publisher_topic


    @staticmethod
    def comparison_with_the_original(fields_dict, data_dict):
        comparison_dictionary = {}
        for field in fields_dict:
            if data_dict[field.key] == data_dict[field.value][field.key]:
                comparison_dictionary[field.key] = True
            else:
                comparison_dictionary[field.key] = False
            return comparison_dictionary

    def calculate_score(self, fields_dict, data_dict):
        comparison_dict = self.comparison_with_the_original(fields_dict, data_dict)
        score = 0
        return score


    def get_score(self, fields_dict):
        events = self.consumer.consumer
        for event in events:
            data = event.value
            score = self.calculate_score(fields_dict, data)
            data["score"] = score
            self.producer.publish_message(self.publisher_topic, data)

