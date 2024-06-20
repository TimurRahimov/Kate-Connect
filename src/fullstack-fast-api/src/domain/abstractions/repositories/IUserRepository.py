from abc import ABC, abstractmethod

from src.domain.entities import UserEntity


class IUserRepository(ABC):

    @abstractmethod
    async def add(self, user_entity: UserEntity):
        pass

    @abstractmethod
    async def query(self, user_id: str) -> UserEntity | None:
        pass

    @abstractmethod
    async def query_all(self) -> dict[str, UserEntity] | None:
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        pass
