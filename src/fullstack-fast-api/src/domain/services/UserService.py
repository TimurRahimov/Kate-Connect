from datetime import datetime
from uuid import uuid4
import random

from src.domain.entities import PasswordEntity, UserEntity
from src.domain.exceptions import (AuthenticationError, UserNotFoundError, UserWithThisNameExistsError,
                                   PublicKeyNotFoundError)
from src.domain.abstractions.services import IUserService, ISessionService
from src.domain.abstractions.repositories import (IPublicKeyRepository, IUserRepository, IPasswordRepository,
                                                  ISessionRepository)
from src.domain.models import PublicKeyModel, UserModel, SessionModel
from src.utils.time import iso_time, time_iso


class UserService(IUserService):

    def __init__(self,
                 session_service: ISessionService,
                 publickey_repo: IPublicKeyRepository,
                 user_repo: IUserRepository,
                 password_repo: IPasswordRepository,
                 session_repo: ISessionRepository):
        self.__session_service = session_service
        self.__publickey_repo = publickey_repo
        self.__user_repo = user_repo
        self.__password_repo = password_repo
        self.__session_repo = session_repo

    async def get_user(self, user_id: str, session: SessionModel = None) -> UserModel:
        user = await self.__user_repo.query(user_id)
        return UserModel(
            user_id=user.user_id,
            nickname=user.nickname,
            avatar_link=user.avatar_link,
            last_time_online=iso_time(user.last_time_online),
            online=(await self.get_online(user_id))[0],
            session=session if session and session.user_id == user_id else None
        )

    async def get_online(self, user_id: str) -> tuple[bool, str]:
        user = await self.__user_repo.query(user_id)
        last_time_online = datetime.fromisoformat(user.last_time_online[:-1]).replace(tzinfo=None)
        return abs((datetime.utcnow() - last_time_online).total_seconds() / 60) < 1, user.last_time_online

    async def get_people(self, count: int) -> list[UserModel]:
        all_users_dict = await self.__user_repo.query_all()
        all_users = list(all_users_dict.values())
        random.shuffle(all_users)

        return [UserModel(
            user_id=user.user_id,
            nickname=user.nickname,
            avatar_link=user.avatar_link,
            last_time_online=iso_time(user.last_time_online),
            friends=[],
            online=(await self.get_online(user.user_id))[0]
        ) for user in all_users[:count]]

    async def login(self, nickname: str, hash_of_password: str) -> UserModel:
        all_users_dict = await self.__user_repo.query_all()
        for user_id, user_entity in all_users_dict.items():
            if user_entity.nickname == nickname:
                user_password = await self.__password_repo.query(user_id)
                if user_password.hash_of_password == hash_of_password:
                    session = await self.__session_service.create_session(user_id)
                    user_entity.last_time_online = time_iso(session.last_activity)
                    await self.__user_repo.add(user_entity)

                    return UserModel(
                        user_id=user_id,
                        nickname=user_entity.nickname,
                        avatar_link=user_entity.avatar_link,
                        session=session,
                        last_time_online=session.last_activity,
                        online=(await self.get_online(user_entity.user_id))[0])
                else:
                    raise AuthenticationError()
        raise UserNotFoundError()

    async def register(self, nickname: str, hash_of_password: str) -> UserModel:
        all_users_dict = await self.__user_repo.query_all()
        for user_id, user_entity in all_users_dict.items():
            if user_entity.nickname == nickname:
                raise UserWithThisNameExistsError()

        user_id = uuid4().hex
        session = await self.__session_service.create_session(user_id)

        user_entity = UserEntity(user_id=user_id, nickname=nickname, last_time_online=time_iso(session.last_activity))
        password_entity = PasswordEntity(user_id=user_id, hash_of_password=hash_of_password)

        await self.__user_repo.add(user_entity)
        await self.__password_repo.add(password_entity)

        return UserModel(
            user_id=user_id,
            nickname=nickname,
            last_time_online=session.last_activity,
            session=session,
            online=True)

    async def logout(self, session: SessionModel):
        try:
            await self.__session_service.delete_session(session)
        except ValueError:
            pass
        except UserNotFoundError:
            pass

    async def edit_user(self, session: SessionModel, param: str, value: str) -> bool:
        if not await self.__session_service.verify(session):
            return False

        user = await self.__user_repo.query(session.user_id)

        if param == 'nickname':
            user.nickname = value
        elif param == 'hash_of_password':
            user.hash_of_password = value
        elif param == 'avatar_link':
            user.avatar_link = value

        await self.__user_repo.add(user)
        return True

    async def get_publickey(self, user_id: str) -> str:
        public_key = await self.__publickey_repo.query(user_id)
        if not public_key:
            raise PublicKeyNotFoundError
        return public_key.public_key

    async def set_publickey(self, user_id: str,
                            hash_of_password: str,
                            publickey: str):
        password = await self.__password_repo.query(user_id)
        if password.hash_of_password != hash_of_password:
            raise AuthenticationError
        await self.__publickey_repo.add(PublicKeyModel(user_id, publickey))
