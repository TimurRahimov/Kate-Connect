from enum import Enum
from pydantic import BaseModel


class MainWsRequestType(Enum):
    CHAT: str = 'chat'
    MESSAGE: str = 'message'
    NOTIFICATION: str = 'notification'
    ONLINE: str = 'online'


class MainWsRequestAction(Enum):
    SEND: str = 'send'
    GET: str = 'get'


class MainWsRequestChatData(BaseModel):
    chat_id: str
    oldest_message_id: str
    offset: int
    count: int


class MainWsRequest(BaseModel):
    command_type: MainWsRequestType
    action: MainWsRequestAction
    data: MainWsRequestChatData | None
