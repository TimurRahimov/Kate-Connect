from src.domain.abstractions.repositories import IUserRepository
from src.domain.entities import UserEntity
from src.infrastructure.KateDB import IDataBase


class UserRepository(IUserRepository):

    def __init__(self, kate_db: IDataBase):
        self.__user_table = kate_db.get_table(entity_type=UserEntity)

    async def add(self, user_entity: UserEntity):
        await self.__user_table.add(user_entity.user_id, user_entity)

    async def query(self, user_id: str) -> UserEntity | None:
        return await self.__user_table.query(user_id)

    async def query_all(self) -> dict[str, UserEntity] | None:
        return await self.__user_table.query_all()

    async def delete(self, user_id: str) -> bool:
        return await self.__user_table.delete(user_id)
