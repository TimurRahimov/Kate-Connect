from abc import ABC, abstractmethod

from src.domain.entities import FriendEntity
from src.domain.models import SessionModel


class IFriendService(ABC):

    @abstractmethod
    async def add_friend(self, session: SessionModel, friend_id: str) -> bool:
        pass

    @abstractmethod
    async def confirm_friend(self, session: SessionModel, friend_id: str) -> bool:
        pass

    @abstractmethod
    async def get_friends(self, session: SessionModel, user_id: str = None) -> list[FriendEntity | None]:
        pass

    @abstractmethod
    async def delete_friend(self, session: SessionModel, friend_id: str) -> bool:
        pass
