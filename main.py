import pika
import Environment as Environment
import src.callbacks as callbacks

from pika.channel import Channel
from pika.connection import Connection
from src.database.MongoDBConnection import get_db
from src.config.queue import config

db = get_db(Environment.MONGODB_DB)

if Environment.COLLECTION_SENSORS_NAME not in db.list_collection_names():
    print(f"Creating {Environment.COLLECTION_SENSORS_NAME} collection")
    db.create_collection(Environment.COLLECTION_SENSORS_NAME,
                         expireAfterSeconds=604800,
                         timeseries={
                                'timeField': "timestamp",
                                'metaField': "metadata",
                                'granularity': "minutes"
                            })

def on_open(connection: Connection):
   connection.channel(on_open_callback = on_channel_open)


def on_channel_open(channel: Channel):
   channel.basic_consume(Environment.RABBITMQ_DEFAULT_TOPIC, callbacks.default_topic_callback, auto_ack = True)
   channel.basic_consume(Environment.RABBITMQ_SYSTEM_QUEUE, callbacks.system_queue_callback, auto_ack = True)

queue_config = config[Environment.SQS_DRIVE]
parameters = pika.URLParameters(queue_config['url'])

connection = pika.SelectConnection(parameters = parameters, on_open_callback = on_open)

try:
   connection.ioloop.start()
except KeyboardInterrupt:
   connection.close()
   connection.ioloop.start()