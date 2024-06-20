from abc import ABC, abstractmethod

from src.domain.models import SessionModel, MessageType, AttachmentModel, MessageModel


class IMessageService(ABC):

    @abstractmethod
    async def send_message(self, session: SessionModel, chat_id: str,
                           message_type: MessageType = MessageType.SIMPLE,
                           encodings: dict[str, str] = None,
                           attachments: list[AttachmentModel] = None) -> MessageModel | None:
        """
        from_id = session.user_id
        encodings - for_id, encoding
        Автоматически: message_id, timestamp, shown, edited
        """
        pass

    @abstractmethod
    async def get_message(self, session: SessionModel, chat_id: str, message_id: str) -> MessageModel | None:
        pass

    @abstractmethod
    async def set_attachments(self, session: SessionModel, chat_id: str, message_id: str,
                              attachments: list[AttachmentModel] = None) -> MessageModel | None:
        pass

    @abstractmethod
    async def set_encoding(self, session: SessionModel, chat_id: str, message_id: str, for_id: str,
                           encoding: str) -> MessageModel | None:
        """
        Если session.user_id = MessageModel.from_id И
        Если encoding уже существует И существующий отличается от аргумента, то меняем и edited = True
        """
        pass

    @abstractmethod
    async def set_shown(self, session: SessionModel, chat_id: str, message_id: str) -> MessageModel | None:
        """
        Если session.user_id != MessageModel.from_id, добавляем session.user_id в shown_list
        """
        pass

    @abstractmethod
    async def query_messages(self, session: SessionModel, chat_id: str, offset: int, count: int) -> list[MessageModel]:
        """
        offset - величина отступа от самого последнего сообщения
        count - количество последних сообщений
        """
        pass
