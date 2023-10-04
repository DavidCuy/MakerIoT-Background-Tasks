import Environment as env

config = {
    'rabbitmq': {
        'user': env.RABBITMQ_USER,
        'pass': env.RABBITMQ_PASS,
        'host': env.RABBITMQ_HOST,
        'port': env.RABBITMQ_PORT,
        'url': env.RABBITMQ_URL
    }
}