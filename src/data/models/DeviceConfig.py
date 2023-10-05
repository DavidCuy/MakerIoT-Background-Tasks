from datetime import datetime
from mongoengine import IntField, DateTimeField, StringField, DictField, BooleanField

from .mongo.BaseModelMongo import BaseMongoModel

class DeviceConfig(BaseMongoModel):
    name = StringField(required=True, max_length=200)
    device_id = IntField(required=True)
    input_topic = StringField(max_length=512)
    input_json = DictField()
    output_json = DictField()
    output_topic = StringField(max_length=512)
    save_output = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    def before_update(self, *args, **kwargs):
        self.updated_at = datetime.now()
