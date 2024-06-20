from src.domain.abstractions.repositories import IChatRepository
from src.domain.entities import ChatEntity, UserChatsEntity
from src.infrastructure.KateDB import IDataBase


class ChatRepository(IChatRepository):

    def __init__(self, kate_db: IDataBase):
        self.__chat_table = kate_db.get_table(entity_type=ChatEntity)
        self.__user_chat_table = kate_db.get_table(entity_type=UserChatsEntity)

    async def add(self, chat_entity: ChatEntity):
        await self.__chat_table.add(chat_entity.chat_id, chat_entity)
        for member_id in chat_entity.members:
            user_chats = await self.__user_chat_table.query(member_id)
            if user_chats is None:
                user_chats = UserChatsEntity(
                    user_id=member_id,
                    chats=[chat_entity.chat_id]
                )
            else:
                user_chats.chats.append(chat_entity.chat_id)
            await self.__user_chat_table.add(member_id, user_chats)

    async def get_user_chats_id(self, user_id: str) -> list[str]:
        user_chats = await self.__user_chat_table.query(user_id)
        if user_chats is None:
            return {}
        return [chat_id for chat_id in user_chats.chats]

    async def query(self, chat_id: str) -> ChatEntity | None:
        return await self.__chat_table.query(chat_id)

    async def delete(self, chat_id: str) -> bool:
        return await self.__chat_table.delete(chat_id)

    async def delete_member_from_chat(self, chat_id: str, member_id: str):
        user_chats = await self.__user_chat_table.query(member_id)
        if user_chats is not None:
            if chat_id in user_chats.chats:
                user_chats.chats.remove(chat_id)
        await self.__user_chat_table.add(member_id, user_chats)
