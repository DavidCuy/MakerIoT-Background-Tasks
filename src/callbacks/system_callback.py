import json
from typing import cast, List, Dict, Tuple, Type, Any
from src.data.enums import SYSTEM_ACTIONS
import Environment as Environment
import src.mqtt_task as mqtt_task

client = mqtt_task.start()

def publish_message_action(message_channel: str, payload: Dict[str, Any]):
    if not('type' in payload or 'msg_exp' in payload or 'msg_data' in payload or 'title' in payload):
        print("Payload doesn't has the correct format")
        return
    topic = str(Environment.MQTT_SYSTEM_TOPIC).replace('#', message_channel)

    publish_payload = {
        'type': payload['type'],
        'msg_exp': payload['msg_exp'],
        'msg_data': payload['msg_data'],
        'title': payload['title'],
    }
    mqtt_task.publish_message(client, topic, publish_payload)
    


def system_queue_callback(ch, method, properties, body: bytes):
    print(f" [x] Received from {method.routing_key}: {body}")

    try:
        payload : dict = json.loads(str(body.decode('utf-8')))
    except Exception as e:
        print("Is not a valid JSON")
        return
    
    if 'action' not in payload:
        print("action key is required")
        return
    
    action = payload.get('action', '')

    if str(action) == '':
        print('action value could not be empty')
        return
    
    if str(action).lower() == SYSTEM_ACTIONS.PUBLISH_MESSAGE.value:
        channel = payload.get('action_name', SYSTEM_ACTIONS.PUBLISH_MESSAGE.value)
        publish_message_action(channel, payload)

