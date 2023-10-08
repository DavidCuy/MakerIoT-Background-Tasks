import json
from typing import cast, List, Dict, Tuple, Type
import Environment as Environment
import src.mqtt_task as mqtt_task

client = mqtt_task.start()


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

