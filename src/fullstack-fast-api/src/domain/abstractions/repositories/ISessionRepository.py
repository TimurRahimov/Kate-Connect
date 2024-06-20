from abc import ABC, abstractmethod

from src.domain.entities import SessionEntityContainer


class ISessionRepository(ABC):

    @abstractmethod
    async def add(self, session_entity_container: SessionEntityContainer):
        pass

    @abstractmethod
    async def query(self, user_id: str) -> SessionEntityContainer | None:
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        pass
