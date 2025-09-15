import time

from utils.kafka_objects.producer import Producer
from Gemini_Service.GenAPI import GenAPI
import os


class Manager:

    def __init__(self):
        self.GenAPI = GenAPI()
        self.Producer = Producer()
        self.Topic = os.getenv('FIRST_TOPIC')
        self.MainPath = os.getenv('MAIN_PATH')

    def run(self):
        list_of_files = self.list_of_files()
        for file_name in list_of_files:
            image_data = self.GenAPI.open_image_for_send(file_name)
            response = self.GenAPI.get_details_from_gemini(image_data)
            result = self.GenAPI.convert_to_dict(response)
            self.Producer.publish_message(topic=self.Topic, message=result)
            time.sleep(30)

    def list_of_files(self):
        return [os.path.join(self.MainPath, file_name) for file_name in os.listdir(self.MainPath)]