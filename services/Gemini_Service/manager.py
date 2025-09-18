from utils.mongo_client.connection import Connection
from utils.kafka_objects.producer import Producer
from utils.kafka_objects.consumer import Consumer
from utils.mongo_client.dal import MongoDAL
from services.Gemini_Service.GenAPI import GenAPI
from pymongo import MongoClient
from utils.log.logger import Logger
import os


class Manager:

    def __init__(self):
        self.GenAPI = GenAPI()
        self.Logger = Logger.get_logger()

        self.MainPath = os.getenv('MAIN_PATH')
        self.ProduceTopic = os.getenv('FIRST_TOPIC')
        self.ConsumeTopic = os.getenv('ID_TOPIC')
        self.Group = os.getenv('KAFKA_GEMINI_GROUP')

        self.Producer = Producer()
        self.Consumer = Consumer(self.Group, [self.ConsumeTopic])

        self.MongoConnectionString = os.getenv('MONGO_CONNECTION_STRING')
        self.MongoDB = os.getenv('MONGO_DB_NAME')

        self.MongoClient = MongoClient(self.MongoConnectionString)
        self.Connection = Connection(client=self.MongoClient, db_name=self.MongoDB)
        self.MongoDal = MongoDAL(self.Connection)

    def run(self):
        events = self.Consumer.consumer
        for event in events:
            image_id = event.value
            try:
                file_readed = self.MongoDal.get_binary(image_id)
                self.Logger.info('fetch the image from mongo succeed')

                try:
                    image_data = self.GenAPI.read_image_for_send(file=file_readed)
                    response = self.GenAPI.get_details_from_gemini(image_data)
                    result = self.GenAPI.convert_to_dict_response_and_id(response, image_id)
                    self.Logger.info('Gemini processed the image')

                    try:
                        self.Producer.publish_message(topic=self.ProduceTopic, message=result)
                        self.Logger.info('Producer publish the details')
                    except:
                        self.Logger.error('Producer not complete the publish')

                except Exception as e:
                    self.Logger.error(f'Gemini not processed the image {e}')

            except:
                self.Logger.error('fetch image from mongo not complete')

