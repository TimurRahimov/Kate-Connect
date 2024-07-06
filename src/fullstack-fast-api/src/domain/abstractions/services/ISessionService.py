from abc import ABC, abstractmethod

from src.domain.models import SessionModel


class ISessionService(ABC):

    @abstractmethod
    async def create_session(self, user_id: str) -> SessionModel | None:
        pass

    @abstractmethod
    async def delete_session(self, session: SessionModel) -> bool:
        pass

    @abstractmethod
    async def get_sessions(self, user_id: str) -> list[SessionModel] | None:
        pass

    @abstractmethod
    async def verify(self, session: SessionModel) -> SessionModel:
        pass
