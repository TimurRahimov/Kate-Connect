from abc import ABC, abstractmethod

from src.domain.abstractions.event_buses import IEventConsumer
from src.domain.models import MessageModel


class IRealTimeEventBus(ABC):

    @abstractmethod
    async def connect(self, connection_id: str, consumer: IEventConsumer):
        pass

    @abstractmethod
    async def disconnect(self, connection_id: str):
        pass

    @abstractmethod
    async def new_message_event(self, connection_id: str, message_model: MessageModel):
        pass
