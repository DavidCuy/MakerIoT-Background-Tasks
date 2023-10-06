import Environment
from paho.mqtt.client import Client, MQTTMessage
from src.config.mqtt import config
from src.data.enums import MQTT_AUTH_METHOD
from src.data.models import DeviceConfig

mqtt_conf = config[Environment.MQTT_LIB]

def start():
    def on_connect(client: Client, userdata, flags: dict, rc: int):
        """ Callback que se ejecuta cuando el cliente de MQTT se conecta correctamente al Host

        Args:
            client (Client): Cliente de MQTT
            userdata (any): Datos de sesion del usuario
            flags (dict): [description]
            rc (int): [description]
        """
        print(f"Connected with result code {str(rc)}")

    def on_message(client: Client, userdata, message: MQTTMessage):
        """ Callback que se ejecuta cada vez que recibe un mensaje de alguno de los topicos a los que se subscribio

        Args:
            client (Client): Cliente de MQTT
            userdata ([type]): [description]
            message (MQTTMessage): Mensaje que viene a traves del topico
        """
        print("Message from topic: {}".format(message.topic))

    client = Client()

    if str(mqtt_conf['auth-method']).upper() == MQTT_AUTH_METHOD.USER_PASS.value:
        client.username_pw_set(username=mqtt_conf['user'], password=mqtt_conf['pass'])

    client.on_connect = on_connect
    client.on_message = on_message
    print('Subscribing to mosquitto')
    client.connect(host=mqtt_conf['host'], port=mqtt_conf['port'])

    client.loop_start()

    return client


def subscribe_topic(client: Client, config: DeviceConfig):
    client.subscribe(config.input_topic)
