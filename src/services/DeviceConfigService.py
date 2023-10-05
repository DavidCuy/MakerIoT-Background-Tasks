from .mongo.BaseMongoService import BaseMongoService
from ..data.models import DeviceConfig


class DeviceConfigService(BaseMongoService):
    def __init__(self) -> None:
        super().__init__(DeviceConfig)
