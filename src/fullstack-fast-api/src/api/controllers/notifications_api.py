from fastapi import Body, Request, APIRouter
from src.dependency_injection import ServiceContainer
from src.domain.abstractions.services import INotificationService
from src.utils.session import get_session_from_request

router_notifications_api = APIRouter(prefix="/api/v1/notifications")


@router_notifications_api.get("")
async def get_notifications(request: Request, limit: int = None, offset: int = 0, order: bool = True):
    session = await get_session_from_request(request)

    notification_service = ServiceContainer.get(INotificationService)

    notifications = await notification_service.get_notifications(session)
    notifications = sorted(notifications, key=lambda x: x.timestamp, reverse=order)

    return [n.to_dict() for n in notifications]


@router_notifications_api.put("")
async def shown_notification(request: Request, notification_id: str = Body(...)):
    session = await get_session_from_request(request)
    notification_service = ServiceContainer.get(INotificationService)
    return await notification_service.shown_notification(session, notification_id)


@router_notifications_api.delete("")
async def delete_notification(request: Request, notification_id: str = Body(...)):
    session = await get_session_from_request(request)
    notification_service = ServiceContainer.get(INotificationService)
    await notification_service.delete_notification(session, notification_id)
