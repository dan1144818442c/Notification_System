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
            if data_dict[field.key] == data_dict[field.value]:
                comparison_dictionary[field.key] = True
            else:
                comparison_dictionary[field.key] = False
            return comparison_dictionary

    def calculate_score(self, fields_dict, data_dict):
        comparison_dict = self.comparison_with_the_original(fields_dict, data_dict)




    def get_score(self, fields_dict, data_dict):
        events = self.consumer.consumer
        for event in events:
            data = json.loads(event.value)
            score_dictionary = self.comparison_with_the_original(fields_dict, data_dict)
            self.producer.publish_message(self.publisher_topic, json.dumps(score_dictionary))

