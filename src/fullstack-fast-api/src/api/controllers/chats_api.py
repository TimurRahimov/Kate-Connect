from fastapi import APIRouter, Request

from src.dependency_injection import ServiceContainer
from src.domain.abstractions.services import IChatService
from src.domain.models import ChatModel
from src.utils.session import get_session_from_request

router_chats_api = APIRouter(prefix="/api/v1/chats")


@router_chats_api.get("")
async def get_chat(request: Request, chat_id: str) -> ChatModel:
    session = await get_session_from_request(request)
    chat_service = ServiceContainer.get(IChatService)
    return await chat_service.get_chat(session, chat_id)
