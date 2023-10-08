from src.data.models import DeviceConfig
from src.services import DeviceConfigService

from typing import cast, List, Dict, Tuple, Type
import Environment as Environment
import src.mqtt_task as mqtt_task

service = DeviceConfigService()
client = mqtt_task.start()

subscribed_configs: Dict[str, DeviceConfig] = {}

def validate_config(config: DeviceConfig):
    if config.input_topic == '' or config.input_topic == None:
        return False
    
    if config.input_json == None or config.input_json == '':
        return False
    
    if config.output_topic == '' or config.output_topic == None:
        return False
    
    if config.output_json == None or config.output_json == '':
        return False
    
    sel_conf = subscribed_configs.get(str(config.to_dict()['_id']), None)
    if sel_conf is None:
        return True
    
    sel_conf = sel_conf.to_dict()
    
    change_udpate = False
    for key in sel_conf.keys():
        compare_val = config.to_dict().get(key, None)
        if str(sel_conf[key]) != str(compare_val):
            change_udpate = True
            print(f"Property {key} for object [{sel_conf['_id']}] change")
    
    return change_udpate

def filter_configs():
    _, mongo_configs = cast(Tuple[Type[DeviceConfig], List[DeviceConfig]], service.get_all(paginate=False))
    
    for d_conf in mongo_configs:
        if validate_config(d_conf):
            print(f"Should subscribe input {d_conf.input_topic} to {d_conf.output_topic}")
            mqtt_task.subscribe_topic(client, d_conf)
            subscribed_configs.update({str(d_conf.to_dict()['_id']): d_conf})


def callback(ch, method, properties, body: bytes):
    print(f" [x] Received from {method.routing_key}: {body}")
    filter_configs()


filter_configs()