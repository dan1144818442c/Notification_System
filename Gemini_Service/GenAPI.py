from google.genai import types
from google import genai
import json
import os

class GenAPI:

    def __init__(self):
        self.API_KEY = os.getenv('GEMINI_API_KEY')
        self.Prompt = os.getenv('PROMPT_HOLDER')
        self.Client = genai.Client()

    @staticmethod
    def read_image_for_send(file):
        image_bytes = file
        return image_bytes

    def get_details_from_gemini(self, image_data):
        schema = types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "model": types.Schema(type=types.Type.STRING),
                            "color": types.Schema(type=types.Type.STRING),
                            "number": types.Schema(type=types.Type.INTEGER),
                            "type": types.Schema(type=types.Type.STRING),
                        },
                        required=["model", "color", "number", "type"]
                    )

        response = self.Client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(
                    data=image_data,
                    mime_type='image/jpeg',
                ),
                self.Prompt
            ],
            config = types.GenerateContentConfig(
                response_mime_type="application/json",  # נכריח JSON
                response_schema=schema  # נכריח מבנה
            )
        )
        return response.text

    @staticmethod
    def convert_to_dict_response_and_id(result, image_id):
        result = json.loads(result)
        result['image_id'] = image_id
        return result