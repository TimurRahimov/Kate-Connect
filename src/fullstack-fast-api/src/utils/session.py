from fastapi import Request, WebSocket

from src.domain.exceptions import AuthenticationError
from src.domain.models import SessionModel


async def get_session_from_request(request: Request) -> SessionModel:
    logged_id = request.cookies.get("userId")
    session_id = request.cookies.get("sessionId")

    if logged_id is None or session_id is None:
        raise AuthenticationError()

    return SessionModel(user_id=logged_id, session_id=session_id)


async def get_session_from_websocket(websocket: WebSocket) -> SessionModel:
    logged_id = websocket.cookies.get("userId")
    session_id = websocket.cookies.get("sessionId")

    if logged_id is None or session_id is None:
        raise AuthenticationError()

    return SessionModel(user_id=logged_id, session_id=session_id)
