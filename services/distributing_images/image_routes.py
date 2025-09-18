from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from utils.mongo_client import dal, connection
from services.distributing_images import config
from utils.kafka_objects.producer import Producer
from utils.log.logger import Logger
from fastapi.responses import Response
import uvicorn
from  pymongo import MongoClient

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    content = await file.read()
    logger = Logger().get_logger()
    try:
        client = MongoClient(config.MONGO_CONNECTION_STRING)
        con =  connection.Connection(client = client, db_name= config.MONGO_DB_NAME)
        mongo_conn = dal.MongoDAL(con)
        file_id = mongo_conn.insert_binary(content)
        logger.info(f"Saved file in Mongo with ID {file_id}")
        try:
            Producer().publish_message(config.ID_TOPIC, file_id)
            return 'upload produce complete successfully'
        except Exception as e:
            logger.error(f"Failed to send to kafka: {e}")
            return 'send to kafka not complete successfully'
    except Exception as e:
        logger.error(f"Error uploading image to mongo: {e}")
        return 'upload to mongo not complete successfully'


@app.get("/image/{image_id}")
async def get_image(image_id: str):
    logger = Logger().get_logger()
    print(image_id)
    try:
        client = MongoClient(config.MONGO_CONNECTION_STRING)
        mongo_conn = connection.Connection(client, config.MONGO_DB_NAME)
        file_data = dal.MongoDAL(mongo_conn).get_binary(image_id)

        if not file_data:
            logger.error("file not found")

        return Response(content=file_data, media_type="application/octet-stream")

    except Exception as e:
        logger.error(f"Retrieval from Mongo failed : {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)




