from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from src.domain.exceptions import (AuthenticationError,
                                   PublicKeyNotFoundError,
                                   UserNotFoundError, CompanionsMessageError, UserWithThisLoginExistsError)
from src.front import error_404_page, error_500_page


async def authentication_error_handler(request: Request,
                                       exc: AuthenticationError):
    return JSONResponse(
        status_code=401,
        content={
            "message": f"Ошибка авторизации"
        }
    )


async def pk_not_found_error_handler(request: Request,
                                     exc: PublicKeyNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "message": f"Публичный ключ запрашиваемого пользователя не найден"
        }
    )


async def user_not_found_error_handler(request: Request,
                                       exc: UserNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "message": f"Пользователь не найден"
        }
    )


async def companion_msg_error_handler(request: Request,
                                      exc: CompanionsMessageError):
    return JSONResponse(
        status_code=400,
        content={
            "message": f"Идентификатор получателя в сообщении не совпадает "
                       f"с идентификатором получателя в теле запроса"
        }
    )


async def user_with_this_login_exists_error_handler(request: Request,
                                                    exc: UserWithThisLoginExistsError):
    return JSONResponse(
        status_code=400,
        content={
            "message": "Пользователь с таким логином уже существует"
        }
    )


async def page_not_found(request: Request,
                         exc: HTTPException):
    return await error_404_page(request)


async def internal_server_error(request: Request,
                                exc: HTTPException):
    return await error_500_page(request)
