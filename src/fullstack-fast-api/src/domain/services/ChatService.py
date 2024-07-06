from uuid import uuid4

from src.domain.abstractions.repositories import IChatRepository
from src.domain.abstractions.services import IChatService, ISessionService, IUserService
from src.domain.entities import ChatEntity
from src.domain.models import SessionModel, ChatType, ChatModel


class ChatService(IChatService):

    def __init__(self, session_service: ISessionService,
                 user_service: IUserService,
                 chat_repo: IChatRepository):
        self.__session_service = session_service
        self.__user_service = user_service
        self.__chat_repo = chat_repo

    async def create_chat(self, session: SessionModel, members_id: list[str], chat_type: ChatType,
                          title: str = None, avatar_url: str = "") -> ChatModel | None:
        session = await self.__session_service.verify(session)
        if not session.confirmed:
            return

        if session.user_id in members_id:
            members_id.remove(session.user_id)

        members_id = list(set(members_id))
        members_id.append(session.user_id)

        members_model = []
        for member_id in members_id:
            member_model = await self.__user_service.get_user(member_id, session)
            if member_model is not None:
                members_model.append(member_model)

        if len(members_model) == 1:
            user_chats_id = await self.__chat_repo.get_user_chats_id(session.user_id)
            user_chats = [await self.__chat_repo.query(chat_id) for chat_id in user_chats_id]
            chat_type = ChatType.SELF_CHAT
            for chat_entity in user_chats:
                if chat_entity.chat_type == ChatType.SELF_CHAT:
                    return ChatModel(
                        chat_id=chat_entity.chat_id,
                        chat_type=chat_entity.chat_type,
                        members=members_model,
                        title=chat_entity.title,
                        avatar_url=chat_entity.avatar_url
                    )
        elif len(members_model) == 2:
            user_chats_id = await self.__chat_repo.get_user_chats_id(session.user_id)
            user_chats = [await self.__chat_repo.query(chat_id) for chat_id in user_chats_id]
            for chat_entity in user_chats:
                for member_id in members_id:
                    if member_id != session.user_id and member_id in chat_entity.members:
                        return ChatModel(
                            chat_id=chat_entity.chat_id,
                            chat_type=chat_entity.chat_type,
                            members=members_model,
                            title=chat_entity.title,
                            avatar_url=chat_entity.avatar_url
                        )

        chat_entity = ChatEntity(
            chat_id=uuid4().hex,
            chat_type=chat_type,
            members=[member.user_id for member in members_model],
            title=title,
            avatar_url=avatar_url
        )

        await self.__chat_repo.add(chat_entity)

        return ChatModel(
            chat_id=chat_entity.chat_id,
            chat_type=chat_entity.chat_type,
            members=members_model,
            title=chat_entity.title,
            avatar_url=chat_entity.avatar_url
        )

    async def get_chat(self, session: SessionModel, chat_id: str) -> ChatModel | None:
        session = await self.__session_service.verify(session)
        if not session.confirmed:
            return

        chat_entity = await self.__chat_repo.query(chat_id)
        if chat_entity is not None:
            members_model = []
            for member_id in chat_entity.members:
                member_model = await self.__user_service.get_user(member_id, session)
                if member_model is not None:
                    members_model.append(member_model)

            return ChatModel(
                chat_id=chat_entity.chat_id,
                chat_type=chat_entity.chat_type,
                members=members_model,
                title=chat_entity.title,
                avatar_url=chat_entity.avatar_url
            )

    async def get_user_chats(self, session: SessionModel) -> list[ChatModel] | None:
        user_chats_id = await self.__chat_repo.get_user_chats_id(session.user_id)
        return [await self.get_chat(session, chat_id) for chat_id in user_chats_id]

    async def edit_chat(self, session: SessionModel, chat_id: str, param: str, value: str) -> bool:
        pass

    async def delete_chat(self, session: SessionModel, chat_id: str) -> bool:
        session = await self.__session_service.verify(session)
        if not session.confirmed:
            return False

        return await self.__chat_repo.delete(chat_id)
