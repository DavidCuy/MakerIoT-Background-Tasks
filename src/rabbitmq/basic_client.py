import pika
from src.config.queue import config

class BasicPikaClient:

    def __init__(self, driver='rabbitmq'):
        queue_config = config[driver]
        parameters = pika.URLParameters(queue_config['url'])
        print(queue_config['url'])

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

class BasicMessageReceiver(BasicPikaClient):
    def get_message(self, queue):
        method_frame, header_frame, body = self.channel.basic_get(queue)
        if method_frame:
            print(method_frame, header_frame, body)
            self.channel.basic_ack(method_frame.delivery_tag)
            return method_frame, header_frame, body
        else:
            print('No message returned')
    
    def consume_messages(self, queue, func_callback):
        self.channel.basic_consume(queue=queue, on_message_callback=func_callback, auto_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def close(self):
        self.channel.close()
        self.connection.close()