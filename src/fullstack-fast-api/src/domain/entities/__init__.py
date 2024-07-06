from typing import Optional

from pydantic import BaseModel

from src.domain.models import NotificationType, ChatType, AttachmentType, MessageType


class UserEntity(BaseModel):
    user_id: str
    nickname: str
    avatar_link: str = ""
    last_time_online: Optional[str]


class PasswordEntity(BaseModel):
    user_id: str
    hashed_password: str


class SessionEntity(BaseModel):
    user_id: str
    session_id: str
    last_activity: Optional[str]


class SessionEntityContainer(BaseModel):
    user_id: str
    sessions: dict[str, SessionEntity]


class FriendEntity(BaseModel):
    user_id: str
    friend_id: str
    friend_name: str = ""
    request: bool = False
    confirmed: bool = False
    private: bool = False


class NotificationEntity(BaseModel):
    notification_id: str
    user_id: str
    timestamp: str
    notification_type: NotificationType
    notification_text: str
    data: dict = {}
    shown: str = False


class NotificationEntityContainer(BaseModel):
    user_id: str
    notifications: dict[str, NotificationEntity]


class MessageAttachmentEntity(BaseModel):
    attachment_id: str
    message_id: str
    attachment_type: AttachmentType
    attachment_url: str


class MessageEncodingEntity(BaseModel):
    encoding_id: str
    chat_id: str
    message_id: str
    for_id: str
    encoding: str


class MessageEntity(BaseModel):
    """
    Параметр encodings представляет собой словарь, в котором в качестве
    ключей используются user_id, а в качестве значения encoding_id.
    Параметр attachments представляет собой словарь, в котором в качестве
    ключей используются attachment_id, а в качестве значения MessageAttachmentEntity
    """
    message_id: str
    from_id: str
    chat_id: str
    timestamp: str
    message_type: MessageType = MessageType.SIMPLE
    shown_list: list[str] = []
    edited: bool = False
    encodings: dict[str, str] = {}
    attachments: dict[str, MessageAttachmentEntity] = {}


class MessageContainerEntity(BaseModel):
    chat_id: str
    part: int
    messages: list[MessageEntity] = []


class ChatEntity(BaseModel):
    chat_id: str
    chat_type: ChatType
    members: list[str]
    title: str | None = None
    avatar_url: str = ""


class UserChatsEntity(BaseModel):
    """
    Параметр chats представляет собой словарь:
    ключи - chat_id
    значения - список из участников
    """
    user_id: str
    chats: list[str]
