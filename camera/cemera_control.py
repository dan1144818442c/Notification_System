import os
import requests
from config import *
from log.logger import Logger

logger = Logger.get_logger("camera_control")




for filename in os.listdir(FOLDER_PATH):
    file_path = os.path.join(FOLDER_PATH, filename)
    if os.path.isfile(file_path):
        logger.info(f"Uploading {filename} to {URL_CONNECT}")
        with open(file_path, "rb") as f:
            files = {"file": f}
            try:
                response = requests.post(URL_CONNECT, files=files)
                logger.info(f"Response status code: {response.status_code}")
            except Exception as e:
                logger.error(f"Failed to upload {filename}: {e}")
                continue
