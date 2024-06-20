from abc import ABC, abstractmethod

from src.domain.entities import MessageEncodingEntity


class IEncodingRepository(ABC):

    @abstractmethod
    async def add(self, encoding_entity: MessageEncodingEntity):
        pass

    @abstractmethod
    async def query(self, message_id: str, for_id: str) -> MessageEncodingEntity | None:
        pass

    @abstractmethod
    async def delete(self, message_id: str, for_id: str) -> bool:
        pass
