from src.data.models import DeviceConfig
from src.services import DeviceConfigService

from typing import cast, List, Tuple, Type
import Environment as Environment
import src.mqtt_task as mqtt_task

service = DeviceConfigService()
client = mqtt_task.start()

subscribed_configs: List[DeviceConfig] = []

def validate_config(config: DeviceConfig):
    if config.input_topic == '' or config.input_topic == None:
        return False
    
    if config.input_json == None or config.input_json == '':
        return False
    
    if config.output_topic == '' or config.output_topic == None:
        return False
    
    if config.output_json == None or config.output_json == '':
        return False
    
    return True

def filter_configs():
    _, mongo_configs = cast(Tuple[Type[DeviceConfig], List[DeviceConfig]], service.get_all(paginate=False))
    config_ids = [conf.to_dict()['_id'] for conf in subscribed_configs]
    new_configs = list(filter(lambda conf: conf.to_dict()['_id'] not in config_ids, mongo_configs))
    
    for d_conf in new_configs:
        if validate_config(d_conf):
            print(f"Should subscribe input {d_conf.input_topic} to {d_conf.output_topic}")
            mqtt_task.subscribe_topic(client, d_conf)
            subscribed_configs.append(d_conf)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)    
    filter_configs()


filter_configs()