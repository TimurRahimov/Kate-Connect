from abc import ABC, abstractmethod
from typing import Any


class IEventConsumer(ABC):

    @abstractmethod
    async def send_obj(self, obj: Any):
        pass

    @abstractmethod
    async def send_text(self, data: str):
        pass
