from src.domain.abstractions.repositories import IMessageRepository
from src.domain.entities import MessageEntity, ChatEntity, MessageContainerEntity
from src.infrastructure.KateDB import IDataBase

MAX_MESSAGES_IN_CONTAINER = 300


class MessageRepository(IMessageRepository):

    def __init__(self, kate_db: IDataBase):
        self.__messages_table = kate_db.get_table('messages')

    async def add(self, message_entity: MessageEntity):
        message_container_table = self.__messages_table.inner_table(message_entity.chat_id, MessageContainerEntity)
        message_containers: dict[str, MessageContainerEntity] = await message_container_table.query_all()

        if message_containers is None:
            return []

        sorted_message_containers = sorted(message_containers.items())

        await self.__messages_table.acquire_transaction(message_entity.chat_id)
        try:
            if len(sorted_message_containers) != 0:
                messages_container: MessageContainerEntity = sorted_message_containers[-1][1]
                if len(messages_container.messages) > MAX_MESSAGES_IN_CONTAINER:
                    messages_container = MessageContainerEntity(
                        chat_id=message_entity.chat_id,
                        part=messages_container.part + 1,
                        messages=[message_entity]
                    )
                else:
                    messages_container.messages.append(message_entity)
            else:
                messages_container = MessageContainerEntity(
                    chat_id=message_entity.chat_id,
                    part=0,
                    messages=[message_entity]
                )
            await message_container_table.add(messages_container.chat_id + f'_{messages_container.part}',
                                              messages_container)

        finally:
            await self.__messages_table.release_transaction(message_entity.chat_id)

    async def update(self, message_entity: MessageEntity):
        message_container_table = self.__messages_table.inner_table(message_entity.chat_id, MessageContainerEntity)
        message_containers: dict[str, MessageContainerEntity] = await message_container_table.query_all()

        if message_containers is None:
            return

        await self.__messages_table.acquire_transaction(message_entity.chat_id)
        updated = False
        try:
            for message_container in message_containers.values():
                for message_index in range(len(message_container.messages)):
                    if message_container.messages[message_index].message_id == message_entity.message_id:
                        message_container.messages[message_index] = message_entity
                        await message_container_table.add(message_container.chat_id + f'_{message_container.part}',
                                                          message_container)
                        updated = True
                        break
                if updated:
                    break
        finally:
            await self.__messages_table.release_transaction(message_entity.chat_id)

    async def query(self, chat_id: str, message_id: str) -> MessageEntity | None:
        chat_container_table = self.__messages_table.inner_table(chat_id, MessageContainerEntity)
        message_containers: dict[str, MessageContainerEntity] = await chat_container_table.query_all()

        for message_container in message_containers.values():
            for message in message_container.messages:
                if message.message_id == message_id:
                    return message

    async def query_last(self, chat_id: str, count: int) -> list[MessageEntity]:
        """
        Порядок возвращения: [..., предпоследнее, последнее]
        """
        chat_container_table = self.__messages_table.inner_table(chat_id, MessageContainerEntity)
        message_containers: dict[str, MessageContainerEntity] = await chat_container_table.query_all()

        if message_containers is None:
            return []

        sorted_message_containers = sorted(message_containers.items())
        if len(sorted_message_containers) != 0:
            last_message_container: MessageContainerEntity = sorted_message_containers[-1][1]
            if count == -1:
                return last_message_container.messages
            else:
                return last_message_container.messages[-count:]
        return []

    async def delete(self, chat_id: str, message_id: str) -> bool:
        chat_container_table = self.__messages_table.inner_table(chat_id, MessageContainerEntity)
        message_containers: dict[str, MessageContainerEntity] = await chat_container_table.query_all()

        if message_containers is None:
            return False

        await self.__messages_table.acquire_transaction(chat_id)
        updated = False
        try:
            for message_container in message_containers.values():
                for message_index in range(len(message_container.messages)):
                    if message_container.messages[message_index].message_id == message_id:
                        del message_container.messages[message_index]
                        await chat_container_table.add(message_container.chat_id + f'_{message_container.part}',
                                                       message_container)
                        updated = True
                        break
                if updated:
                    break
        finally:
            await self.__messages_table.release_transaction(chat_id)
