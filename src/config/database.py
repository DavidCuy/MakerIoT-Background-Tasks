import Environment as env

config = {
    'pymongo': {
        'username': env.MONGODB_USER,
        'password': env.MONGODB_PASS,
        'database': env.MONGODB_DB,
        'host': env.MONGODB_HOST,
        'port': env.MONGODB_PORT,
        'url': env.MONGODB_URL
    }
}