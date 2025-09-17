from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from utils.kafka_objects.consumer import Consumer
from utils.log.logger import Logger

logger = Logger.get_logger()


TOPICS = ["final_results_for_car"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        consumer = Consumer(topics= TOPICS, group_id="route_group")
        app.state.current_message = consume_generator(consumer)
    except Exception as e:
        logger.error(f"Error can't consume to kafka: {e}")
    yield


def consume_generator(consumer:Consumer):
    for message in consumer.consumer:
        print(message.offset)
        yield message.value


app = FastAPI(lifespan=lifespan)
# app.state.current_message = None



@app.get('/')
def get_results():
    if app.state.current_message is not None:
        current_message = next(app.state.current_message)
        return current_message
    else:
        return {"message:": "Error - can't consume events from kafka"}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
