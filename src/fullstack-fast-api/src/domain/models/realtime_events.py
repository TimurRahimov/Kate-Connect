from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from src.domain.models import UserModel, MessageType, ChatModel, AttachmentModel, MessageModel
from src.utils.time import time_iso


class RealTimeEventType(Enum):
    NEW_MESSAGE = "new_message"
    GET_MESSAGE_RESULT = "get_message_result"
    GET_CHATS_RESULT = "get_chats_result"


@dataclass(frozen=True)
class MessageEventModel:
    message_id: str
    from_user: UserModel
    chat: ChatModel
    timestamp: datetime
    encoding: str
    message_type: MessageType = MessageType.SIMPLE
    attachments: list[AttachmentModel] = field(default_factory=dict)

    def to_dict(self):
        return {
            'message_id': self.message_id,
            'from_user': self.from_user.to_dict(),
            'chat': self.chat.to_dict(),
            'timestamp': time_iso(self.timestamp),
            'encoding': self.encoding,
            'message_type': self.message_type.value,
            'attachments': [a.to_dict() for a in self.attachments]
        }


@dataclass(frozen=True)
class GetMessageEventModel:
    messages: list[MessageModel]

    def to_dict(self):
        return {
            'messages': [m.to_dict() for m in self.messages]
        }


@dataclass(frozen=True)
class GetChatsEventModel:
    chats: list[ChatModel]
    last_messages: dict[str, MessageModel]

    def to_dict(self):
        return {
            'chats': [c.to_dict() for c in self.chats],
            'last_messages': {
                chat_id: message.to_dict() for chat_id, message in self.last_messages.items()
            }
        }


@dataclass(frozen=True)
class RealTimeEventModel:
    event_type: RealTimeEventType
    data: MessageEventModel | GetMessageEventModel | GetChatsEventModel

    def to_dict(self):
        return {
            'event_type': self.event_type.value,
            'data': self.data.to_dict()
        }
