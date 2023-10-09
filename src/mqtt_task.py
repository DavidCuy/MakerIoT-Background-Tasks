import json
import Environment
import traceback
from typing import Any, Dict
from datetime import datetime
from paho.mqtt.client import Client, MQTTMessage
from mathjspy import MathJS
from src.config.mqtt import config
from src.data.enums import MQTT_AUTH_METHOD
from src.data.models import DeviceConfig
from src.database.MongoDBConnection import get_collection, get_db

mqtt_conf = config[Environment.MQTT_LIB]
subscribed_configs: Dict[str, DeviceConfig] = {}

math_js = MathJS()

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
        try:
            payload = json.loads(str(message.payload.decode('utf-8')))
        except Exception as e:
            print("Is not a valid JSON")
            return
        print("Message from topic: {}".format(message.topic))
        configs_input_topics = [conf.input_topic for conf in subscribed_configs.values()]
        selected_conf = list(filter(lambda conf: conf.input_topic in configs_input_topics, subscribed_configs.values()))

        if len(selected_conf) < 1: return

        selected_conf = selected_conf[0]
        output_conf: Dict = selected_conf.to_dict()['output_json']

        output_payload = {}

        key = ""
        try:
            for key in output_conf.keys():
                math_js.update(payload)
                output_payload[key] = round(math_js.eval(output_conf[key]), 4)

            client.publish(selected_conf.output_topic, json.dumps(output_payload))

        except Exception as e:
            print(f"Ocurrio un error con el contenido de las llaves [{key}]")
            traceback.print_exc()
            return
        
        if selected_conf.save_output:
            if Environment.COLLECTION_SENSORS_NAME in get_db(Environment.MONGODB_DB).list_collection_names():
                sensors_collection = get_collection(Environment.MONGODB_DB, Environment.COLLECTION_SENSORS_NAME)
                sorted_payload = dict(sorted(output_payload.items()))
                sensors_collection.insert_one({
                    "metadata": {
                        "deviceId": selected_conf.device_id
                    },
                    "timestamp": datetime.now(),
                    **sorted_payload
                })

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
    subscribed_configs.update({str(config.to_dict()['_id']): config})


def publish_message(client: Client, topic: str, payload: Dict[str, Any]):
    client.publish(topic, json.dumps(payload))
    print(f"Message published to {topic}")
