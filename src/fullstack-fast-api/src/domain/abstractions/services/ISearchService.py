from abc import ABC, abstractmethod

from src.domain.models import UserModel, SessionModel


class ISearchService(ABC):

    @abstractmethod
    async def user_search(self, session: SessionModel, search_string: str = None, **kwargs) -> list[UserModel | None]:
        pass
