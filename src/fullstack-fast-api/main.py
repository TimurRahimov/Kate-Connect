from subprocess import Popen

import os
import uvicorn
from fastapi import FastAPI
from src.api.exceptions_handlers import (authentication_error_handler, user_not_found_error_handler,
                                         pk_not_found_error_handler, companion_msg_error_handler,
                                         user_with_this_login_exists_error_handler, page_not_found, internal_server_error)
from src.api.web_sockets.v1 import router_ws_v1
from src.domain.exceptions import (AuthenticationError, UserNotFoundError, PublicKeyNotFoundError,
                                   CompanionsMessageError, UserWithThisLoginExistsError)
from src.front.file_accessers import router_files

from src.infrastructure import InfrastructureRegister
from src.domain import DomainRegister

from src.api.controllers import (router_notifications_api, router_search_api, router_people_api, router_users_api,
                                 router_messages_api, router_chats_api)
from src.front.page_builders import router_front

InfrastructureRegister.register()
DomainRegister.register()

app = FastAPI(
    title="Kate Connect"
)
app.include_router(router_notifications_api)
app.include_router(router_people_api)
app.include_router(router_search_api)
app.include_router(router_users_api)
app.include_router(router_ws_v1)
app.include_router(router_front)
app.include_router(router_files)
app.include_router(router_messages_api)
app.include_router(router_chats_api)

# Exception Handlers
app.add_exception_handler(AuthenticationError, authentication_error_handler)
app.add_exception_handler(PublicKeyNotFoundError, pk_not_found_error_handler)
app.add_exception_handler(UserNotFoundError, user_not_found_error_handler)
app.add_exception_handler(CompanionsMessageError, companion_msg_error_handler)
app.add_exception_handler(UserWithThisLoginExistsError, user_with_this_login_exists_error_handler)
app.add_exception_handler(404, page_not_found)
app.add_exception_handler(500, internal_server_error)

if __name__ == '__main__':
    KC_PORT = int(os.environ["KC_PORT"])
    KC_IP = os.environ["KC_IP"]
    # Popen(['python3', '-m', 'https_redirect'])
    # uvicorn.run(
    #     'main:app', port=443, host='192.168.0.2',
    #     reload=True, loop="asyncio",
    #     ssl_keyfile='ssl/kateconnect.key',
    #     ssl_certfile='ssl/kateconnect.crt')

    uvicorn.run(
        'main:app', port=KC_PORT, host=KC_IP,
        reload=True, loop="asyncio")

# from pydantic import BaseSettings, Field


# class Settings(BaseSettings):
#     auth_key: str
#     url: str = Field(..., env="URL")
#
#
# print(Settings().dict())

# async def middleware(request: Request, call_next):
#     print(await request.body())
#     response = await call_next(request)
#     print(response)
#     return response
#
#
# app.middleware("http")(middleware)
