from src.domain.abstractions.repositories import ISessionRepository
from src.domain.entities import SessionEntityContainer
from src.infrastructure.KateDB import IDataBase


class SessionRepository(ISessionRepository):

    def __init__(self, kate_db: IDataBase):
        self.__session_table = kate_db.get_table(entity_type=SessionEntityContainer)

    async def add(self, session_entity_container: SessionEntityContainer):
        await self.__session_table.add(session_entity_container.user_id, session_entity_container)

    async def query(self, user_id: str) -> SessionEntityContainer | None:
        return await self.__session_table.query(user_id)

    async def delete(self, user_id: str) -> bool:
        return await self.__session_table.delete(user_id)

