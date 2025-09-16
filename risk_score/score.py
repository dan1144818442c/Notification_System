from utils.kafka_objects.consumer import Consumer
from utils.kafka_objects.producer import Producer
from utils.mongo_client.dal import MongoDAL
from utils.mongo_client.dal import Connection
from pymongo import MongoClient
import config
from datetime import datetime, timedelta

import json


class RiskScore:
    def __init__(self, topics:list[str], publisher_topic):
        self.topics = topics
        self.consumer = Consumer(topics = topics, group_id="risk_score_group")
        self.producer = Producer()
        self.publisher_topic = publisher_topic

        self.client_mongo = MongoClient()
        self.connection = Connection(self.client_mongo ,db_name= config.MONGO_DB_NAME)
        self.dal_mongo = MongoDAL(connection=self.connection)


    @staticmethod
    def comparison_with_the_original(fields_dict, data_dict):
        comparison_dictionary = {}
        for key, value in fields_dict.items():
            if data_dict[key] in data_dict[value][key]:
                comparison_dictionary[key] = True
            else:
                comparison_dictionary[key] = False
            return comparison_dictionary

    def calculate_score(self, fields_dict, data_dict):
        comparison_dict = self.comparison_with_the_original(fields_dict, data_dict)

        score = sum(comparison_dict.values())
        times_enter = self.calculate_score_of_enters(self.get_list_of_time_enters(car_id = data_dict['number']))
        if times_enter > 3 :
            score = (score +( 0.5 * (times_enter -3))) / (len(data_dict) + 1)
        else:
            score = score / len(data_dict)


        return score * 100


    def get_list_of_time_enters(self , car_id):
        list_doc = self.dal_mongo.find_documents(collection_name=config.MONGO_COLLECTION_NAME , query={"car_id": car_id} )
        return list_doc

    def calculate_score_of_enters(self , list_of_enters):
        now = datetime.now()
        time_window = timedelta(hours=1, minutes=30)  # שעה וחצי אחורה

        for e in list_of_enters:
            e["entry_time"] = datetime.fromisoformat(e["entry_time"])

        now = datetime.now(datetime.utcnow().astimezone().tzinfo)  # עם timezone
        time_window = timedelta(hours=1, minutes=30)

        recent_entries = [e for e in list_of_enters if (now - e["entry_time"]) <= time_window]

        return len(recent_entries)

    def get_score(self, fields_dict):
        events = self.consumer.consumer
        for event in events:
            print(event)
            data = event.value
            score = self.calculate_score(fields_dict, data)
            data["score"] = score
            self.producer.publish_message(self.publisher_topic, data)
            print(f"Published data with score {data} to topic {self.publisher_topic}")


# a = RiskScore("A" , "s")
# a.get_list_of_time_enters()