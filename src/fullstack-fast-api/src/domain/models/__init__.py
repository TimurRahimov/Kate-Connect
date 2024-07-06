from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from src.utils.time import time_iso, iso_time


class AttachmentType(Enum):
    MUSIC = 1  # Музыка
    PHOTO = 2  # Фотография
    VIDEO = 3  # Видео
    FILE = 4  # Файл


class ChatType(Enum):
    PERSONAL_CHAT = 1  # Персональный чат
    GROUP_CHAT = 2  # Групповой чат
    CHANNEL = 3  # Канал
    BOT_CHAT = 4  # Чат с ботом
    ANONYMOUS_CHAT = 5  # Чат с анонимностью
    SECRET_CHAT = 6  # Секретный чат
    SELF_CHAT = 7  # Беседа с самим собой


class MessageType(Enum):
    SIMPLE = 1  # Обыкновенное сообщение
    FORWARDED = 2  # Пересланное сообщение


class NotificationType(Enum):
    ADD_FRIEND = 1  # О запросе дружбы
    CONFIRMED_FRIEND = 2  # О подтверждении дружбы
    DELETE_FRIEND = 3  # Об удалении из списка друзей


@dataclass(frozen=True)
class FriendModel:
    user_id: str
    friend_id: str
    friend_name: str = ""
    request: bool = False
    confirmed: bool = False
    private: bool = False

    @classmethod
    def from_dict(cls, _dict: dict):
        return cls(
            user_id=_dict['user_id'],
            friend_id=_dict['friend_id'],
            friend_name=_dict['friend_name'],
            request=_dict['request'],
            confirmed=_dict['confirmed'],
            private=_dict['private']
        )

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'friend_id': self.friend_id,
            'friend_name': self.friend_name,
            'request': self.request,
            'confirmed': self.confirmed,
            'private': self.private,
        }


@dataclass(frozen=True)
class SessionModel:
    user_id: str
    session_id: str
    last_activity: Optional[datetime] = None
    confirmed: bool = False

    def confirm(self) -> 'SessionModel':
        return SessionModel(
            user_id=self.user_id,
            session_id=self.session_id,
            last_activity=self.last_activity,
            confirmed=True
        )

    def set_last_activity(self, last_activity: datetime):
        return SessionModel(
            user_id=self.user_id,
            session_id=self.session_id,
            last_activity=last_activity,
            confirmed=self.confirmed
        )


@dataclass(frozen=True)
class UserModel:
    user_id: str
    nickname: str
    avatar_link: str = ""
    session: Optional[SessionModel] = None
    last_time_online: Optional[datetime] = None
    friends: list[FriendModel | None] = field(default_factory=list)
    online: bool = False

    @classmethod
    def from_dict(cls, _dict: dict):
        return cls(
            user_id=_dict['user_id'],
            nickname=_dict['nickname'],
            avatar_link=_dict['avatar_link'],
            last_time_online=iso_time(_dict['last_time_online']),
            friends=[FriendModel.from_dict(f) for f in _dict['friends']],
            online=_dict['online']
        )

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'nickname': self.nickname,
            'avatar_link': self.avatar_link,
            'last_time_online': time_iso(self.last_time_online),
            'friends': [f.to_dict() for f in self.friends],
            'online': self.online
        }


@dataclass(frozen=True)
class PublicKeyModel:
    user_id: str
    public_key: str


@dataclass(frozen=True)
class PasswordModel:
    user_id: str
    password: str


@dataclass(frozen=True)
class AttachmentModel:
    attachment_id: str
    message_id: str
    attachment_type: AttachmentType
    attachment_url: str

    def to_dict(self):
        return {
            'attachment_id': self.attachment_id,
            'message_id': self.message_id,
            'attachment_type': self.attachment_type.value,
            'attachment_url': self.attachment_url
        }


@dataclass(frozen=True)
class EncodingModel:
    encoding_id: str
    chat_id: str
    message_id: str
    for_id: str
    encoding: str

    def to_dict(self):
        return {
            'encoding_id': self.encoding_id,
            'chat_id': self.chat_id,
            'message_id': self.message_id,
            'for_id': self.for_id,
            'encoding': self.encoding
        }


@dataclass(frozen=True)
class ChatModel:
    chat_id: str
    chat_type: ChatType
    members: list[UserModel]
    title: str | None = None
    avatar_url: str = ""

    def to_dict(self):
        return {
            "chat_id": self.chat_id,
            "chat_type": self.chat_type.value,
            "members": [u.to_dict() for u in self.members],
            "title": self.title,
            "avatar_url": self.avatar_url
        }


@dataclass(frozen=True)
class MessageModel:
    message_id: str
    from_user: UserModel
    chat_id: str
    timestamp: datetime
    encodings: dict[str, EncodingModel]
    chat: ChatModel = None
    message_type: MessageType = MessageType.SIMPLE
    shown_list: list[str] = field(default_factory=dict)
    edited: bool = False
    attachments: list[AttachmentModel] = field(default_factory=dict)

    def to_dict(self):
        return {
            'message_id': self.message_id,
            'from_user': self.from_user.to_dict(),
            'chat_id': self.chat_id,
            'timestamp': time_iso(self.timestamp),
            'encodings': {e.for_id: e.to_dict() for e in self.encodings.values()},
            'message_type': self.message_type.value,
            'shown_list': self.shown_list,
            'edited': self.edited,
            'attachments': [a.to_dict() for a in self.attachments]
        }


@dataclass(frozen=True)
class NotificationModel:
    user_id: str
    notification_type: NotificationType
    notification_text: str
    data: dict[str, ...] = field(default_factory=dict)
    notification_id: str | None = None
    timestamp: datetime | None = None
    shown: str = False

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'notification_type': self.notification_type.value,
            'notification_text': self.notification_text,
            'data': self.data,
            'notification_id': self.notification_id,
            'timestamp': time_iso(self.timestamp),
            'shown': self.shown
        }
