import json
import decimal
import datetime
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import List
import Environment as env
from src.config.database import config

config_mongo = config[env.MONGODB_DRIVER]

conn = MongoClient(config_mongo['url'])

def get_db(name: str) -> Database:
    return conn[name]

def get_collection(db_name: str, collection_name: str) -> Collection:
    return conn[db_name][collection_name]