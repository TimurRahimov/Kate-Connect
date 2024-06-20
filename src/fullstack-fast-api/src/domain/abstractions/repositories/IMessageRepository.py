from abc import ABC, abstractmethod

from src.domain.entities import MessageEntity


class IMessageRepository(ABC):

    @abstractmethod
    async def add(self, message_entity: MessageEntity):
        pass

    @abstractmethod
    async def update(self, message_entity: MessageEntity):
        pass

    @abstractmethod
    async def query(self, chat_id: str, message_id: str) -> MessageEntity | None:
        pass

    @abstractmethod
    async def query_last(self, chat_id: str, count: int) -> list[MessageEntity]:
        pass

    @abstractmethod
    async def delete(self, chat_id: str, message_id: str) -> bool:
        pass
