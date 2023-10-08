import Environment as Environment
import src.callbacks as callbacks

from src.rabbitmq import BasicMessageReceiver
from src.database.MongoDBConnection import get_db

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

basic_message_receiver = BasicMessageReceiver(Environment.SQS_DRIVE)

# Consume the message that was sent.
basic_message_receiver.consume_messages(Environment.RABBITMQ_DEFAULT_TOPIC, callbacks.default_topic_callback)

# Close connections.
basic_message_receiver.close()
