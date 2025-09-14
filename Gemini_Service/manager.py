from utils.kafka_objects.producer import Producer
from Gemini_Service.GenAPI import GenAPI
import os


class Manager:

    def __init__(self):
        self.GenAPI = GenAPI()
        self.Producer = Producer()
        self.Topic = os.getenv('FIRST_TOPIC')

    def run(self, image_path):
        image_data = self.GenAPI.open_image_for_send(image_path)
        response = self.GenAPI.get_details_from_gemini(image_data)
        result = self.GenAPI.convert_to_dict(response)
        self.Producer.publish_message(topic=self.Topic, message=result)
