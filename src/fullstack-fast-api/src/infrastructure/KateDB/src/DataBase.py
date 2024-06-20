import json
import os
from typing import Optional, Type, get_args

from .interfaces import IDataBase, ITable, Entity
from .Table import Table


class DataBase(IDataBase):

    def __init__(self, db_name: str, abs_path: str):
        self.db_name = db_name
        self.__db_abs_path = os.path.join(abs_path, db_name)
        self.__tables: dict[str, Table[Entity]] = {}

        if not os.path.exists(self.__db_abs_path):
            os.mkdir(self.__db_abs_path)

        meta_path = os.path.join(self.__db_abs_path, "__meta__.json")
        if not os.path.exists(meta_path):
            self.__meta = {
                'name': self.db_name,
                'version': '1.0.0'
            }
            with open(meta_path, 'w') as f:
                json.dump(self.__meta, f)
        else:
            with open(meta_path) as f:
                self.__meta = json.load(f)

    def root_table(self, table_name: str, entity_type: Type[Entity] = None) -> ITable[Entity]:
        if table_name not in self.__tables:
            self.__tables[table_name] = Table[entity_type](table_name, self.__db_abs_path)
        return self.__tables[table_name]

    def get_table(self, table_name: str = None, entity_type: Type[Entity] = None) -> Optional[ITable[Entity]]:
        if table_name is not None:
            if table_name in self.__tables:
                return self.__tables[table_name]
        elif entity_type is not None:
            for _, entity in self.__tables.items():
                if entity.entity_type == entity_type:
                    return entity

    def delete_table(self, table_name: str) -> bool:
        if table_name in self.__tables:
            del self.__tables[table_name]
        table_path = os.path.join(self.__db_abs_path, table_name)
        if os.path.exists(table_path):
            os.rmdir(table_path)
            return True
        return False
