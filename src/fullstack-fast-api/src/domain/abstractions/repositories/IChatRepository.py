from abc import ABC, abstractmethod

from src.domain.entities import ChatEntity


class IChatRepository(ABC):

    @abstractmethod
    async def add(self, chat_entity: ChatEntity):
        pass

    @abstractmethod
    async def get_user_chats_id(self, user_id: str) -> list[str]:
        pass

    @abstractmethod
    async def query(self, chat_id: str) -> ChatEntity | None:
        pass

    @abstractmethod
    async def delete(self, chat_id: str) -> bool:
        pass

    @abstractmethod
    async def delete_member_from_chat(self, chat_id: str, member_id: str) -> bool:
        pass
