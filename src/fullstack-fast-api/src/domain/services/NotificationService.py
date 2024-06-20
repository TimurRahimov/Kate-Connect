from uuid import uuid4

from src.domain.abstractions.services import INotificationService, ISessionService
from src.domain.entities import NotificationEntity, NotificationEntityContainer
from src.domain.exceptions import AuthenticationError
from src.domain.models import NotificationModel, SessionModel
from src.infrastructure.KateDB import IDataBase
from src.utils.time import utcnow_iso, iso_time


class NotificationService(INotificationService):

    def __init__(self,
                 session_service: ISessionService,
                 kate_db: IDataBase):
        self.__session_service = session_service
        self.__notification_table = kate_db.get_table(entity_type=NotificationEntityContainer)

    async def add_notification(self, notification: NotificationModel):
        notification_container = await self.__notification_table.query(notification.user_id)
        if notification_container is None:
            notification_container = NotificationEntityContainer(user_id=notification.user_id, notifications={})
        notification_id = uuid4().hex
        notification_container.notifications[notification_id] = NotificationEntity(
            notification_id=notification_id,
            user_id=notification.user_id,
            timestamp=utcnow_iso(),
            notification_type=notification.notification_type,
            notification_text=notification.notification_text,
            data=notification.data,
            shown=False
        )
        await self.__notification_table.add(notification.user_id, notification_container)

    async def get_notifications(self, session: SessionModel) -> list[NotificationModel | None]:
        if not await self.__session_service.verify(session):
            raise AuthenticationError()

        notification_container = await self.__notification_table.query(session.user_id)
        if notification_container is None:
            notification_container = NotificationEntityContainer(user_id=session.user_id, notifications={})
            await self.__notification_table.add(session.user_id, notification_container)

        return [
            NotificationModel(
                n.user_id,
                n.notification_type,
                n.notification_text,
                n.data,
                n.notification_id,
                iso_time(n.timestamp),
                n.shown
            )
            for n in notification_container.notifications.values()
        ]

    async def delete_notification(self, session: SessionModel, notification_id: str):
        if not await self.__session_service.verify(session):
            raise AuthenticationError()

        notification_container = await self.__notification_table.query(session.user_id)
        if notification_container.notifications.get(notification_id):
            notification_container.notifications.pop(notification_id)
            await self.__notification_table.add(session.user_id, notification_container)

    async def shown_notification(self, session: SessionModel, notification_id: str):
        if not await self.__session_service.verify(session):
            raise AuthenticationError()

        notification_container = await self.__notification_table.query(session.user_id)
        if notification_container.notifications.get(notification_id):
            notification_container.notifications[notification_id].shown = True
            await self.__notification_table.add(session.user_id, notification_container)
