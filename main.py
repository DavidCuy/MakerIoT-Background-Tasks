from src.rabbitmq import BasicMessageReceiver
import src.Environment as Environment


def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)


basic_message_receiver = BasicMessageReceiver(Environment.SQS_DRIVE)

# Consume the message that was sent.
basic_message_receiver.consume_messages(Environment.RABBITMQ_DEFAULT_TOPIC, callback)

# Close connections.
basic_message_receiver.close()
