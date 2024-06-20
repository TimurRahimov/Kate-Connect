from abc import ABC, abstractmethod

from src.domain.models import ChatModel, ChatType, SessionModel


class IChatService(ABC):

    @abstractmethod
    async def create_chat(self, session: SessionModel, members_id: list[str], chat_type: ChatType,
                          title: str = None, avatar_url: str = "") -> ChatModel | None:
        pass

    @abstractmethod
    async def get_chat(self, session: SessionModel, chat_id: str) -> ChatModel | None:
        pass

    @abstractmethod
    async def get_user_chats(self, session: SessionModel) -> list[ChatModel] | None:
        pass

    @abstractmethod
    async def edit_chat(self, session: SessionModel, chat_id: str, param: str, value: str) -> bool:
        pass

    @abstractmethod
    async def delete_chat(self, session: SessionModel, chat_id: str) -> bool:
        pass
