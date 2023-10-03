import pika

class BasicPikaClient:

    def __init__(self, rabbitmq_broker_host, rabbitmq_user, rabbitmq_password, port="5672"):

        url = f"amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_broker_host}:{port}"
        parameters = pika.URLParameters(url)

        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()