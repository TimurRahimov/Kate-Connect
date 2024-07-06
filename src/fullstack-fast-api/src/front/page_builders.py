import os

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse

from src.dependency_injection import ServiceContainer
from src.domain.abstractions.repositories import IUserRepository
from src.domain.abstractions.services import IUserService, IFriendService, ISessionService, IChatService, \
    IMessageService
from src.domain.models import UserModel, SessionModel, ChatType
from src.domain.exceptions import UserNotFoundError, PublicKeyNotFoundError

TEMPLATES_ABS_PATH = os.path.dirname(os.path.abspath(__file__))

templates = Jinja2Templates(directory=os.path.join(TEMPLATES_ABS_PATH, "templates"))

router_front = APIRouter()


async def get_user(request: Request) -> UserModel | None:
    user_repo = ServiceContainer.get(IUserRepository)

    user_service = ServiceContainer.get(IUserService)
    session_service = ServiceContainer.get(ISessionService)
    friend_service = ServiceContainer.get(IFriendService)

    if "sessionId" in request.cookies:
        session = SessionModel(user_id=request.cookies["userId"], session_id=request.cookies["sessionId"])
        session = await session_service.verify(session)
        if session.confirmed:
            user = await user_repo.query(session.user_id)

            online = await user_service.get_online(user.user_id)
            friends = await friend_service.get_friends(session=session)

            return UserModel(user_id=user.user_id, nickname=user.nickname, avatar_link=user.avatar_link,
                             last_time_online=user.last_time_online, friends=friends, online=online,
                             session=session)


@router_front.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    user = await get_user(request)
    # raise Exception()
    return templates.TemplateResponse("index.html", {"request": request, "user": user})


@router_front.get("/new", response_class=HTMLResponse)
async def index_page(request: Request):
    user = await get_user(request)
    # raise Exception()
    return templates.TemplateResponse("default_page_new.html", {"request": request, "user": user})


@router_front.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    user = await get_user(request)

    if user is not None:
        return RedirectResponse("/", status_code=302)

    return templates.TemplateResponse("login.html", {"request": request, "user": None})


@router_front.get("/people", response_class=HTMLResponse)
async def people_page(request: Request):
    user = await get_user(request)
    return templates.TemplateResponse("people.html", {"request": request, "user": user})


@router_front.get("/connect", response_class=HTMLResponse)
async def connect_page(request: Request, _with: str = None, _to_chat: str = None):
    user = await get_user(request)
    chat_service = ServiceContainer.get(IChatService)
    chat = None
    if _with is not None:
        chat = await chat_service.create_chat(user.session, members_id=[_with], chat_type=ChatType.PERSONAL_CHAT)
        _with = chat.chat_id
        if len(chat.members) == 1:
            _with = chat.members[0].nickname
        elif len(chat.members) == 2:
            if chat.members[0].user_id == user.user_id:
                _with = chat.members[1].nickname
            else:
                _with = chat.members[0].nickname

    if _to_chat is not None:
        return await connect_chat_page(request, _to_chat)

    return templates.TemplateResponse("connect.html", {
        "request": request, "user": user, "_with": _with,
        "chat": chat.to_dict() if chat else chat,
        "show_window": "show_messages_window" if _with else "show_chats_window",
    })


@router_front.get("/connect/{chat_id}", response_class=HTMLResponse)
async def connect_chat_page(request: Request, chat_id: str):
    user = await get_user(request)
    chat_service = ServiceContainer.get(IChatService)
    chat = await chat_service.get_chat(user.session, chat_id)
    _with = None
    show_chats_window = False

    if chat:
        show_chats_window = True
        if len(chat.members) == 1:
            _with = chat.members[0].nickname
        elif len(chat.members) == 2:
            if chat.members[0].user_id == user.user_id:
                _with = chat.members[1].nickname
            else:
                _with = chat.members[0].nickname
        else:
            _with = chat.title

    return templates.TemplateResponse("connect.html", {
        "request": request, "user": user, "_with": _with,
        "chat": chat.to_dict() if chat else chat,
        "show_window": "show_messages_window" if show_chats_window else "show_chats_window",
    })


@router_front.get("/settings", response_class=HTMLResponse)
async def settings_page(request: Request):
    user = await get_user(request)

    if user is None:
        return RedirectResponse('/', status_code=302)

    return templates.TemplateResponse("settings.html", {"request": request, "user": user,
                                                        "last_time_online": user.last_time_online})


@router_front.get("/hello/{name}", response_class=HTMLResponse)
async def hello_page(request: Request, name: str):
    user = await get_user(request)

    return templates.TemplateResponse("hello.html", {"request": request, "name": name, "user": user})


@router_front.get("/{user_id}", response_class=HTMLResponse)
async def user_page(request: Request, user_id: str):
    user = await get_user(request)
    user_service = ServiceContainer.get(IUserService)
    try:
        page_user = await user_service.get_user(user_id, user.session if user else None)
    except UserNotFoundError:
        return await error_404_page(request)

    return templates.TemplateResponse("user_page.html", {"request": request, "user": user,
                                                         "page_user": page_user,
                                                         "last_time_online": page_user.last_time_online})


@router_front.get("/{user_id}/public_key", response_class=HTMLResponse)
async def get_public_key(request: Request, user_id: str):
    user = await get_user(request)
    user_service = ServiceContainer.get(IUserService)
    try:
        public_key = await user_service.get_publickey(user_id)
        return HTMLResponse(content=f"{public_key}")
    except (UserNotFoundError, PublicKeyNotFoundError):
        return await error_404_page(request)


@router_front.get("/{user_id}/avatar")
async def get_avatar_link(request: Request, user_id: str):
    user = await get_user(request)
    user_service = ServiceContainer.get(IUserService)
    page_user = await user_service.get_user(user_id, user.session)
    return RedirectResponse(page_user.avatar_link if page_user.avatar_link else "/images/default_avatar.jpg",
                            status_code=302)


async def error_404_page(request: Request):
    user = await get_user(request)
    return templates.TemplateResponse("404.html", {"request": request, "user": user}, status_code=404)


async def error_500_page(request: Request):
    user = await get_user(request)
    return templates.TemplateResponse("500.html", {"request": request, "user": user}, status_code=500)
