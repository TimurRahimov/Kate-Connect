from src.dependency_injection import ServiceContainer
from .abstractions.services import (IUserService, IFriendService, INotificationService,
                                    ISessionService, ISearchService, IChatService, IMessageService)
from .services import (UserService, FriendService, NotificationService,
                       SessionService, SearchService, ChatService, MessageService)


class DomainRegister:

    @classmethod
    def register(cls):
        ServiceContainer.register(ISessionService, SessionService)
        ServiceContainer.register(INotificationService, NotificationService)
        ServiceContainer.register(IUserService, UserService)
        ServiceContainer.register(IFriendService, FriendService)
        ServiceContainer.register(ISearchService, SearchService)
        ServiceContainer.register(IChatService, ChatService)
        ServiceContainer.register(IMessageService, MessageService)
