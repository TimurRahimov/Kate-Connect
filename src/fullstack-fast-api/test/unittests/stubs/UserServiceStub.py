from src.domain.abstractions.repositories import IPublicKeyRepository
from src.domain.abstractions.services import ISessionService
from src.domain.services import UserService
from unittest.mock import Mock, MagicMock

from src.infrastructure.KateDB import IDataBase


class UserServiceStub(UserService):

    def __init__(self):
        pass
        self.session_service: Mock | ISessionService = Mock(ISessionService)
        self.publickey_repo: Mock | IPublicKeyRepository = Mock(IPublicKeyRepository)
        self.kate_db: Mock | IDataBase = Mock(IDataBase)
        super().__init__(self.session_service, self.publickey_repo, self.kate_db)
