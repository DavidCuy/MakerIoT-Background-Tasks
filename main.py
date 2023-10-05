import json
from src.rabbitmq import BasicMessageReceiver
from src.data.models import DeviceConfig
from src.services import DeviceConfigService

from typing import cast, List, Tuple, Type
import Environment as Environment

service = DeviceConfigService()

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

    _, all_configs = cast(Tuple[Type[DeviceConfig], List[DeviceConfig]], service.get_all(paginate=False))
    device_configs = list(map(lambda d: d.to_dict(), all_configs))
    print(device_configs)


basic_message_receiver = BasicMessageReceiver(Environment.SQS_DRIVE)

# Consume the message that was sent.
basic_message_receiver.consume_messages(Environment.RABBITMQ_DEFAULT_TOPIC, callback)

# Close connections.
basic_message_receiver.close()
