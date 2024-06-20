from src.domain.abstractions.repositories import IEncodingRepository
from src.domain.entities import MessageEncodingEntity
from src.infrastructure.KateDB import IDataBase


class EncodingRepository(IEncodingRepository):

    def __init__(self, kate_db: IDataBase):
        self.__encodings_table = kate_db.get_table('encodings')

    async def add(self, encoding_entity: MessageEncodingEntity):
        encoding_table = self.__encodings_table.inner_table(encoding_entity.message_id, MessageEncodingEntity)
        await encoding_table.add(encoding_entity.for_id, encoding_entity)

    async def query(self, message_id: str, for_id: str) -> MessageEncodingEntity | None:
        encoding_table = self.__encodings_table.inner_table(message_id, MessageEncodingEntity)
        return await encoding_table.query(for_id)

    async def delete(self, message_id: str, for_id: str) -> bool:
        encoding_table = self.__encodings_table.inner_table(message_id, MessageEncodingEntity)
        return await encoding_table.delete(for_id)
