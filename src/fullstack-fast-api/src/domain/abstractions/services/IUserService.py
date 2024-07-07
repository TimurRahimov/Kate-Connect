from abc import ABC, abstractmethod

from src.domain.models import UserModel, SessionModel, AuthModel


class IUserService(ABC):

    @abstractmethod
    async def get_user(self, user_id: str, session: SessionModel = None) -> UserModel:
        pass

    @abstractmethod
    async def get_online(self, user_id: str) -> tuple[bool, str]:
        pass

    @abstractmethod
    async def get_people(self, count: int) -> list[UserModel]:
        pass

    @abstractmethod
    async def get_login(self, session: SessionModel) -> str:
        pass

    @abstractmethod
    async def login(self, login: str, password: str) -> AuthModel:
        pass

    @abstractmethod
    async def register(self, login: str, password: str) -> UserModel:
        pass

    @abstractmethod
    async def logout(self, session: SessionModel):
        pass

    @abstractmethod
    async def edit_user(self, session: SessionModel, param: str, value: str) -> bool:
        pass

    @abstractmethod
    async def get_publickey(self, user_id: str) -> str:
        pass

    @abstractmethod
    async def set_publickey(self, user_id: str,
                            hash_of_password: str,
                            publickey: str):
        pass
