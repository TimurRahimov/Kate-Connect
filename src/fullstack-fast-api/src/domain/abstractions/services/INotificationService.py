from abc import ABC, abstractmethod

from src.domain.models import NotificationModel, SessionModel


class INotificationService(ABC):

    @abstractmethod
    async def add_notification(self, notification: NotificationModel):
        pass

    @abstractmethod
    async def get_notifications(self, session: SessionModel) -> list[NotificationModel | None]:
        pass

    @abstractmethod
    async def delete_notification(self, session: SessionModel, notification_id: str):
        pass

    @abstractmethod
    async def shown_notification(self, session: SessionModel, notification_id: str):
        pass
