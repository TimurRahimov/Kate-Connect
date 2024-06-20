import asyncio
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.api.web_sockets.request_handlers import MainWsRequestHandler
from src.api.web_sockets.requests import MainWsRequest, MainWsRequestType, MainWsRequestAction
from src.dependency_injection import ServiceContainer
from src.domain.abstractions.event_buses import IRealTimeEventBus
from src.domain.abstractions.services import ISessionService, INotificationService, IUserService, IMessageService
from src.domain.exceptions import AuthenticationError
from src.domain.models import SessionModel
from src.domain.models.realtime_events import GetMessageEventModel, RealTimeEventModel, RealTimeEventType
from src.infrastructure.event_buses import EventConsumer
from src.utils.session import get_session_from_websocket

router_ws_v1 = APIRouter()


@router_ws_v1.websocket("/ws/v1/")
async def main_ws(websocket: WebSocket):
    session_service = ServiceContainer.get(ISessionService)
    user_service = ServiceContainer.get(IUserService)
    notification_service = ServiceContainer.get(INotificationService)
    message_service = ServiceContainer.get(IMessageService)
    realtime_eventbus = ServiceContainer.get(IRealTimeEventBus)

    session = await get_session_from_websocket(websocket)
    if session.user_id is None or session.session_id is None:
        raise AuthenticationError()

    if not await session_service.verify(session):
        return

    await websocket.accept()

    request_handler = MainWsRequestHandler(websocket, session)
    await realtime_eventbus.connect(session.user_id, EventConsumer(websocket))

    try:
        while True:
            request_string = await websocket.receive_text()
            request = MainWsRequest.parse_raw(request_string)
            await request_handler.handle(request)

    except WebSocketDisconnect:
        await realtime_eventbus.disconnect(session.user_id)


@router_ws_v1.websocket("/ws/v1/notifications")
async def get_notifications_ws(websocket: WebSocket):
    logged_id = websocket.cookies.get("userId")
    session_id = websocket.cookies.get("sessionId")
    if logged_id is None or session_id is None:
        raise AuthenticationError()

    session = SessionModel(user_id=logged_id, session_id=session_id)

    session_service = ServiceContainer.get(ISessionService)
    notification_service = ServiceContainer.get(INotificationService)

    if not await session_service.verify(session):
        return

    await websocket.accept()

    try:
        while True:
            text = await websocket.receive_text()
            request = json.loads(text)
            response = []

            newest_notification_id = request['newest_notification_id']

            notifications = await notification_service.get_notifications(session)
            notifications = sorted(notifications, key=lambda x: x.timestamp, reverse=True)
            for n in notifications:
                if n.notification_id != newest_notification_id:
                    response.append(n.to_dict())
                else:
                    break
            # [n for n in notifications if n.timestamp]

            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        pass


@router_ws_v1.websocket("/ws/v1/online")
async def get_online_ws(websocket: WebSocket):
    logged_id = websocket.cookies.get("userId")
    session_id = websocket.cookies.get("sessionId")
    if logged_id is None or session_id is None:
        raise AuthenticationError()

    session = SessionModel(user_id=logged_id, session_id=session_id)

    session_service = ServiceContainer.get(ISessionService)
    user_service = ServiceContainer.get(IUserService)

    if not await session_service.verify(session):
        return

    await websocket.accept()

    try:
        while True:
            text = await websocket.receive_text()
            request: dict = json.loads(text)
            response = {}

            users_for_check_list: list = request['users_for_check']

            for user_id in users_for_check_list:
                user_online_tuple = await user_service.get_online(user_id)
                response[user_id] = {
                    'online': user_online_tuple[0],
                    'last_time_online': user_online_tuple[1]
                }

            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        pass
