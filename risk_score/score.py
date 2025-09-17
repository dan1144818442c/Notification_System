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
        try:
            for key, value in fields_dict.items():
                if data_dict[key].lower() in data_dict[value][key].lower()\
                        or data_dict[value][key].lower() in data_dict[key].lower():
                    comparison_dictionary[key] = True
                else:
                    comparison_dictionary[key] = False
                return comparison_dictionary
        except:
            return {}

    def update_score_and_description(self, fields_dict, data_dict):
        comparison_dict = self.comparison_with_the_original(fields_dict, data_dict)

        data_dict['description'] = ""
        score =  list(comparison_dict.values()).count(False) * 33.33333
        if score:
            score /= len(comparison_dict)
            data_dict['description'] += f"הרכב חשוד כגנוב.\n "

        times_enter = self.calculate_score_of_enters(self.get_list_of_time_enters(car_id = data_dict['number']))
        if times_enter > 3 :
            score += ( 5 * (times_enter -3))
            data_dict['description'] += f"הרכב נראה לאחרונה {times_enter} פעמים \n"


        if  data_dict['is_off_road'] == "true":
            score = score + 33.3333
            data_dict['description'] += f"הרכב ירד מהכביש. "

        if score > 100:
            score = 100
        data_dict['score'] = score
        return data_dict


    def get_list_of_time_enters(self , car_id):
        list_doc = self.dal_mongo.find_documents(collection_name=config.MONGO_COLLECTION_NAME , query={"car_id": car_id} )
        return list_doc

    def calculate_score_of_enters(self , list_of_enters):
        now = datetime.now()
        time_window = timedelta(hours=1, minutes=30)


        now = datetime.now()  # עם timezone
        time_window = timedelta(hours=1, minutes=30)

        recent_entries = [e for e in list_of_enters if (now - e["entry_time"]) <= time_window]

        return len(recent_entries)

    def get_score(self, fields_dict):
        events = self.consumer.consumer
        for event in events:
            print(event)
            data = event.value
            data =self.update_score_and_description(fields_dict, data)
            self.producer.publish_message(self.publisher_topic, data)
            print(f"Published data with score {data} to topic {self.publisher_topic}")
