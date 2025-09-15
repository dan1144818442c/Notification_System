from google.genai import types
from google import genai
import json
import os

class GenAPI:

    def __init__(self):
        self.API_KEY = os.getenv('GEMINI_API_KEY')
        self.Prompt = os.getenv('PROMPT_HOLDER')
        self.Client = genai.Client()


    def open_image_for_send(self, path_file):
        with open(path_file, 'rb') as file:
            image_bytes = file.read()

        return image_bytes

    def get_details_from_gemini(self, image_data):
        response = self.Client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(
                    data=image_data,
                    mime_type='image/jpeg',
                ),
                self.Prompt
            ]
        )
        return response.text

    @staticmethod
    def convert_to_dict(result):
        return json.loads(result.strip('`').strip('json').strip())