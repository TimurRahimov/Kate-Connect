from src.domain.abstractions.services import IFriendService, IUserService, INotificationService, ISessionService
from src.domain.entities import FriendEntity, NotificationType
from src.domain.exceptions import AuthenticationError
from src.domain.models import NotificationModel, SessionModel
from src.infrastructure.KateDB import IDataBase


class FriendService(IFriendService):

    def __init__(self,
                 session_service: ISessionService,
                 user_service: IUserService,
                 notification_service: INotificationService,
                 kate_db: IDataBase):
        self.__session_service = session_service
        self.__user_service = user_service
        self.__notification_service = notification_service
        self.__friend_table = kate_db.get_table('friends')

    async def add_friend(self, session: SessionModel, friend_id: str) -> bool:
        session = await self.__session_service.verify(session)
        if not session.confirmed:
            raise AuthenticationError()

        user = FriendEntity(user_id=session.user_id, friend_id=friend_id)
        friend = FriendEntity(user_id=friend_id, friend_id=session.user_id, request=True)

        for entity in user, friend:
            await self.__friend_table.inner_table(entity.user_id, FriendEntity).add(entity.friend_id, entity)

        await self.__notification_service.add_notification(
            NotificationModel(
                user_id=friend_id,
                notification_type=NotificationType.ADD_FRIEND,
                notification_text=f"{(await self.__user_service.get_user(session.user_id, session)).nickname} "
                                  f"отправил заявку в друзья",
                data={
                    "friend_id": session.user_id,
                    "nickname": (await self.__user_service.get_user(session.user_id, session)).nickname
                }
            )
        )
        # TODO: Сервис должен соответствовать логике сервиса, а не репозитория.
        #  в данный сервис необходимо передавать тип события и дополнительные данные.
        #  Текст уведомления должен создаваться на стороне сервиса

        return True

    async def confirm_friend(self, session: SessionModel, friend_id: str) -> bool:
        session = await self.__session_service.verify(session)
        if not session.confirmed:
            raise AuthenticationError()

        user = await self.__friend_table.inner_table(session.user_id, FriendEntity).query(friend_id)
        friend = await self.__friend_table.inner_table(friend_id).query(session.user_id)

        if not user or not friend:
            return False

        user.confirmed = True
        friend.confirmed = True

        for entity in user, friend:
            await self.__friend_table.inner_table(entity.user_id, FriendEntity).add(entity.friend_id, entity)

        return True

    async def get_friends(self, session: SessionModel, user_id: str = None) -> list[FriendEntity | None]:
        session = await self.__session_service.verify(session)
        if not session.confirmed:
            raise AuthenticationError()

        if user_id is None:
            user_id = session.user_id

        friends = (await self.__friend_table.inner_table(user_id, FriendEntity).query_all()).values()

        if session.user_id != user_id:
            return [f for f in friends if f.confirmed and not f.private or f.user_id == user_id]

        return [f for f in friends]

    async def delete_friend(self, session: SessionModel, friend_id: str) -> bool:
        session = await self.__session_service.verify(session)
        if not session.confirmed:
            raise AuthenticationError()

        await self.__friend_table.inner_table(session.user_id, FriendEntity).delete(friend_id)
        await self.__friend_table.inner_table(friend_id, FriendEntity).delete(session.user_id)

        return True
