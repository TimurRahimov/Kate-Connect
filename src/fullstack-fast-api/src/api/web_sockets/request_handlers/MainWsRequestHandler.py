import json

from fastapi import WebSocket

from src.api.web_sockets.requests import MainWsRequest, MainWsRequestType, MainWsRequestAction
from src.dependency_injection import ServiceContainer
from src.domain.abstractions.services import IMessageService, IChatService
from src.domain.models import SessionModel
from src.domain.models.realtime_events import RealTimeEventModel, RealTimeEventType, GetMessageEventModel, \
    GetChatsEventModel


class MainWsRequestHandler:

    def __init__(self, websocket: WebSocket, session: SessionModel):
        self.__ws = websocket
        self.__session = session
        self.__message_service = ServiceContainer.get(IMessageService)
        self.__chat_service = ServiceContainer.get(IChatService)

    async def handle(self, request: MainWsRequest):
        if request.command_type == MainWsRequestType.CHAT:
            print("CHAT", request.action.value, request.data)
            await self.__handle_chat_request(request)
        elif request.command_type == MainWsRequestType.MESSAGE:
            print("MESSAGE", request.action.value, request.data)
            await self.__handle_message_request(request)
        elif request.command_type == MainWsRequestType.NOTIFICATION:
            print("NOTIFICATION", request.action.value, request.data)
        elif request.command_type == MainWsRequestType.ONLINE:
            print("ONLINE", request.action.value, request.data)

    async def __handle_chat_request(self, request: MainWsRequest):
        if request.action == MainWsRequestAction.GET:
            user_chats = await self.__chat_service.get_user_chats(self.__session)

            last_messages = {}
            for chat in user_chats:
                chat_id = chat.chat_id
                last_message_list = await self.__message_service.query_messages(self.__session, chat_id, 0, 1)
                if len(last_message_list) != 0:
                    last_messages[chat_id] = last_message_list[0]

            realtime_event = RealTimeEventModel(
                RealTimeEventType.GET_CHATS_RESULT,
                GetChatsEventModel(
                    user_chats,
                    last_messages
                )
            )

            await self.__ws.send_text(json.dumps(realtime_event.to_dict()))

    async def __handle_message_request(self, request: MainWsRequest):
        if request.action == MainWsRequestAction.GET:
            chat_id = request.data.chat_id
            oldest_message_id = request.data.oldest_message_id
            offset = request.data.offset
            count = request.data.count

            last_messages = await self.__message_service.query_messages(self.__session, chat_id, offset, count)
            last_messages.reverse()

            messages = []
            for m in last_messages:
                messages.append(m)

            messages.reverse()

            realtime_event = RealTimeEventModel(
                RealTimeEventType.GET_MESSAGE_RESULT,
                GetMessageEventModel(messages)
            )

            await self.__ws.send_text(json.dumps(realtime_event.to_dict()))
