import os

from src.dependency_injection import ServiceContainer
from src.domain.abstractions.repositories import (IPublicKeyRepository, IUserRepository, IPasswordRepository,
                                                  ISessionRepository, IChatRepository, IMessageRepository,
                                                  IEncodingRepository)
from ..domain.abstractions.event_buses import IRealTimeEventBus

from .KateDB import DataBase
from .KateDB.src.interfaces import IDataBase
from .repositories import (PublicKeyRepository, UserRepository, PasswordRepository, SessionRepository, ChatRepository,
                           MessageRepository, EncodingRepository)
from .event_buses import RealTimeEventBus

from ..domain.entities import NotificationEntityContainer, PasswordEntity, SessionEntityContainer, UserEntity, \
    ChatEntity, UserChatsEntity


class InfrastructureRegister:

    @classmethod
    def register(cls):
        ETC_ABS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "etc")

        if not os.path.exists(ETC_ABS_PATH):
            os.mkdir(ETC_ABS_PATH)

        ServiceContainer.register(IDataBase, DataBase, db_name='kate-connect', abs_path=ETC_ABS_PATH)
        kate_db = ServiceContainer.get(IDataBase)
        kate_db.root_table('users', UserEntity)
        kate_db.root_table('sessions', SessionEntityContainer)
        kate_db.root_table('notifications', NotificationEntityContainer)
        kate_db.root_table('passwords', PasswordEntity)
        kate_db.root_table('chats', ChatEntity)
        kate_db.root_table('user_chats', UserChatsEntity)
        kate_db.root_table('friends')
        kate_db.root_table('messages')
        kate_db.root_table('encodings')

        ServiceContainer.register(IUserRepository, UserRepository)
        ServiceContainer.register(IPasswordRepository, PasswordRepository)
        ServiceContainer.register(ISessionRepository, SessionRepository)
        ServiceContainer.register(IPublicKeyRepository, PublicKeyRepository)
        ServiceContainer.register(IChatRepository, ChatRepository)
        ServiceContainer.register(IMessageRepository, MessageRepository)
        ServiceContainer.register(IEncodingRepository, EncodingRepository)

        ServiceContainer.register(IRealTimeEventBus, RealTimeEventBus)
