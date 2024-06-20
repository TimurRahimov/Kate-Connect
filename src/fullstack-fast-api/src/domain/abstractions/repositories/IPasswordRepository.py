from abc import ABC, abstractmethod

from src.domain.entities import PasswordEntity


class IPasswordRepository(ABC):

    @abstractmethod
    async def add(self, password_entity: PasswordEntity):
        pass

    @abstractmethod
    async def query(self, user_id: str) -> PasswordEntity | None:
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        pass
