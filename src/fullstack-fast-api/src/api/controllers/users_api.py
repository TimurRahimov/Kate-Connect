from fastapi import Response, Body, Request, APIRouter
from fastapi.responses import RedirectResponse

from src.dependency_injection import ServiceContainer
from src.domain.abstractions.services import (IUserService, IFriendService)
from src.domain.models import UserModel, FriendModel
from src.utils.session import get_session_from_request

router_users_api = APIRouter()


@router_users_api.get("/api/v1/users/{user_id}/public_key")
async def get_public_key(user_id: str) -> Response:
    user_service = ServiceContainer.get(IUserService)
    public_key = await user_service.get_publickey(user_id)
    return Response(content=public_key)


@router_users_api.post("/api/v1/users/{user_id}/public_key")
async def set_public_key(user_id: str,
                         hash_of_password: str,
                         public_key: str
                         ) -> dict:
    user_service = ServiceContainer.get(IUserService)
    await user_service.set_publickey(user_id, hash_of_password, public_key)
    return {}


@router_users_api.post("/api/v1/users/register")
async def register_user(nickname: str = Body(...),
                        hash_of_password: str = Body(...)) -> UserModel:
    user_service = ServiceContainer.get(IUserService)
    return await user_service.register(nickname=nickname,
                                       hash_of_password=hash_of_password)


@router_users_api.post("/api/v1/users/login")
async def login_user(nickname: str = Body(...),
                     hash_of_password: str = Body(...)) -> UserModel:
    user_service = ServiceContainer.get(IUserService)
    return await user_service.login(nickname=nickname,
                                    hash_of_password=hash_of_password)


@router_users_api.get("/api/v1/users/logout")
async def logout_user(request: Request) -> dict:
    session = await get_session_from_request(request)

    user_service = ServiceContainer.get(IUserService)
    await user_service.logout(session)

    return {}


@router_users_api.get("/api/v1/users/{user_id}")
async def get_user_info(request: Request, user_id: str) -> UserModel:
    session = await get_session_from_request(request)
    user_service = ServiceContainer.get(IUserService)
    return await user_service.get_user(user_id, session)


@router_users_api.put("/api/v1/users/{user_id}/nickname")
async def edit_user_nickname(request: Request,
                             new_nickname: str = Body(...)):
    session = await get_session_from_request(request)
    user_service = ServiceContainer.get(IUserService)
    return await user_service.edit_user(session, 'nickname', new_nickname)


@router_users_api.put("/api/v1/users/{user_id}/avatar_link")
async def edit_user_nickname(request: Request,
                             new_avatar_link: str = Body(...)):
    session = await get_session_from_request(request)
    user_service = ServiceContainer.get(IUserService)
    return await user_service.edit_user(session, 'avatar_link', new_avatar_link)


@router_users_api.get("/api/v1/users/{user_id}/online")
async def check_user_online(request: Request, user_id: str) -> dict:
    user_service = ServiceContainer.get(IUserService)
    user_online_tuple = await user_service.get_online(user_id)
    return {
        'online': user_online_tuple[0],
        'last_time_online': user_online_tuple[1]
    }


@router_users_api.get("/api/v1/users/{user_id}/avatar")
async def get_user_avatar_link(request: Request, user_id: str):
    session = await get_session_from_request(request)

    user_service = ServiceContainer.get(IUserService)
    page_user = await user_service.get_user(user_id, session)

    return RedirectResponse(page_user.avatar_link if page_user.avatar_link else "/images/default_avatar.jpg",
                            status_code=302)


@router_users_api.post("/api/v1/users/{user_id}/avatar")
async def edit_user_avatar_link(request: Request, user_id: str,
                                avatar_link: str = Body(...)):
    session = await get_session_from_request(request)

    user_service = ServiceContainer.get(IUserService)
    await user_service.edit_user(session, avatar_link=avatar_link)

    return {}


@router_users_api.get("/api/v1/users/{user_id}/friends")
async def get_user_friends(request: Request, user_id: str) -> dict[str, FriendModel]:
    session = await get_session_from_request(request)
    friend_service = ServiceContainer.get(IFriendService)
    friends = await friend_service.get_friends(session=session, user_id=user_id)
    return {f.friend_id: f for f in friends}


@router_users_api.post("/api/v1/users/{user_id}/friends")
async def add_user_friend(request: Request, friend_id: str = Body(...)):
    session = await get_session_from_request(request)
    friend_service = ServiceContainer.get(IFriendService)
    return await friend_service.add_friend(session=session, friend_id=friend_id)


@router_users_api.put("/api/v1/users/{user_id}/friends")
async def confirm_user_friend(request: Request,
                              friend_id: str = Body(...),
                              private: bool = Body(default=None),
                              confirmed: bool = Body(default=None)):
    session = await get_session_from_request(request)
    friend_service = ServiceContainer.get(IFriendService)
    return await friend_service.confirm_friend(session=session, friend_id=friend_id)


@router_users_api.delete("/api/v1/users/{user_id}/friends")
async def delete_user_friend(request: Request, friend_id: str = Body(...)):
    session = await get_session_from_request(request)
    friend_service = ServiceContainer.get(IFriendService)
    return await friend_service.delete_friend(session=session, friend_id=friend_id)
