import Environment as Environment
import src.callbacks as callbacks

from src.rabbitmq import BasicMessageReceiver
from src.services import DeviceConfigService



service = DeviceConfigService()

basic_message_receiver = BasicMessageReceiver(Environment.SQS_DRIVE)

# Consume the message that was sent.
basic_message_receiver.consume_messages(Environment.RABBITMQ_DEFAULT_TOPIC, callbacks.default_topic_callback)

# Close connections.
basic_message_receiver.close()
