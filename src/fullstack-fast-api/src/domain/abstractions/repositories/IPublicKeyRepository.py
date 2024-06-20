from abc import ABC, abstractmethod

from src.domain.models import PublicKeyModel


class IPublicKeyRepository(ABC):

    @abstractmethod
    async def add(self, public_key: PublicKeyModel):
        pass

    @abstractmethod
    async def query(self, user_id: str) -> PublicKeyModel | None:
        pass

    @abstractmethod
    async def delete(self, user_id: str) -> bool:
        pass
