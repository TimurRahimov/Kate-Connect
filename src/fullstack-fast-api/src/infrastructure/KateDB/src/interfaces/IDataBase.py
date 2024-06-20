from abc import ABC, abstractmethod
from typing import Optional, Type

from .ITable import ITable, Entity


class IDataBase(ABC):

    @abstractmethod
    def root_table(self, table_name: str, entity_type: Type[Entity] = None) -> ITable:
        pass

    @abstractmethod
    def get_table(self, table_name: str = None, entity_type: Type[Entity] = None) -> Optional[ITable[Entity]]:
        pass

    @abstractmethod
    def delete_table(self, table_name: str) -> bool:
        pass
