from fastapi import APIRouter, Request

from src.dependency_injection import ServiceContainer
from src.domain.abstractions.services import ISearchService
from src.domain.models import UserModel
from src.utils.session import get_session_from_request

router_search_api = APIRouter()


@router_search_api.get("/api/v1/search/users")
async def search_users(request: Request, search_string: str) -> list[UserModel]:
    special_search = ""
    session = await get_session_from_request(request)
    search_service = ServiceContainer.get(ISearchService)
    if search_string in ("/online", "/all"):
        special_search = search_string
        search_string = ""

    search_result = await search_service.user_search(session=session, search_string=search_string)
    if special_search == "/online":
        return [s for s in search_result if s.online]
    return search_result
