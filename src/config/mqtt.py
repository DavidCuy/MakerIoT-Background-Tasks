import Environment as env

config = {
    'paho-mqtt': {
        'user': env.MQTT_USER,
        'pass': env.MQTT_PASS,
        'host': env.MQTT_HOST,
        'port': env.MQTT_PORT,
        'auth-method': env.MQTT_AUTH_METHOD
    }
}