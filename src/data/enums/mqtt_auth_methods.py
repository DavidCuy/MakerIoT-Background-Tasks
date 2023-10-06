from enum import Enum

class MQTT_AUTH_METHOD(Enum):
    NONE = 'NONE'
    USER_PASS = 'USER_PASS'
    TLS_CERT = 'TLS_CERT'