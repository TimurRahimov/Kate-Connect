from src.domain.abstractions.repositories import IPasswordRepository
from src.domain.entities import PasswordEntity
from src.infrastructure.KateDB import IDataBase


class PasswordRepository(IPasswordRepository):

    def __init__(self, kate_db: IDataBase):
        self.__password_table = kate_db.get_table(entity_type=PasswordEntity)

    async def add(self, password_entity: PasswordEntity):
        await self.__password_table.add(password_entity.user_id, password_entity)

    async def query(self, user_id: str) -> PasswordEntity | None:
        return await self.__password_table.query(user_id)

    async def delete(self, user_id: str) -> bool:
        return await self.__password_table.delete(user_id)
