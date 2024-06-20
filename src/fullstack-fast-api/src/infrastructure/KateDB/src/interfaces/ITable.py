from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, Type
from pydantic import BaseModel

Entity = TypeVar('Entity', bound=BaseModel)
_ITable = TypeVar("_ITable", bound="ITable")


class ITable(ABC, Generic[Entity]):

    @abstractmethod
    async def add(self, entity_id: str, entity: Entity):
        pass

    @abstractmethod
    async def query(self, entity_id: str) -> Entity | None:
        pass

    @abstractmethod
    async def query_all(self) -> dict[str, Entity] | None:
        pass

    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        pass

    @abstractmethod
    async def acquire_transaction(self, entity_id: str):
        pass

    @abstractmethod
    async def release_transaction(self, entity_id: str):
        pass

    @abstractmethod
    def inner_table(self, inner_table_name: str, entity_type: Type[Entity] = None) -> 'ITable[Entity]':
        pass

    @abstractmethod
    def get_inner_table(self, inner_table_name: str) -> Optional['ITable[Entity]']:
        pass

    @abstractmethod
    def get_all_inner_tables(self) -> Optional[dict[str, 'ITable[Entity]']]:
        pass

    @abstractmethod
    def delete_inner_table(self, inner_table_name: str) -> bool:
        pass
