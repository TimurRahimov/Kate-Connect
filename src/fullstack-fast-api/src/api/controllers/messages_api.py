from fastapi import Body, Request, APIRouter
from src.dependency_injection import ServiceContainer
from src.domain.abstractions.services import IMessageService
from src.utils.session import get_session_from_request

router_messages_api = APIRouter(prefix="/api/v1/messages")


@router_messages_api.post("/send")
async def send_message(request: Request, chat_id: str = Body(...), encodings: dict[str, str] = Body(...)) -> str:
    session = await get_session_from_request(request)
    message_service = ServiceContainer.get(IMessageService)
    message = await message_service.send_message(session, chat_id=chat_id, encodings=encodings)
    message_id = message.message_id
    # for for_id, encoding in encodings.items():
    #     await message_service.set_encoding(session, chat_id, message_id, for_id, encoding)
    return message_id

# @router_notifications_api.get("/encoding")
# async def add_encoding(request: Request, chat_id: str) -> str:
#     session = await get_session_from_request(request)
#     message_service = ServiceContainer.get(IMessageService)
#     return (await message_service.send_message(session, chat_id=chat_id)).message_id
