import json
import os
from asyncio import Semaphore
from typing import Optional, Generic, Type

import pydantic

from .interfaces import ITable, Entity
from . import __system_files__


class Table(ITable, Generic[Entity]):
    __entity_type_init: Entity = None

    def __init__(self, table_name: str, db_abs_path: str):
        if table_name in __system_files__:
            raise NameError('This name cannot be used')

        self.table_name = table_name
        self.entity_type = self.__entity_type_init
        self.__table_abs_path = os.path.join(db_abs_path, table_name)
        self.__tables: dict[str, Table[Entity]] = {}
        self.__semaphores = {}

        if not os.path.exists(self.__table_abs_path):
            os.mkdir(self.__table_abs_path)

        if not os.path.exists(self.__get_entity_abs_path("__meta__")):
            if self.entity_type is not None and '__fields__' in self.entity_type.__dict__:
                meta = []
                for field in self.entity_type.__dict__['__fields__'].values():
                    meta.append({
                        'name': field.name,
                        'type': str(field.type_),
                        'required': field.required
                    })

                with open(self.__get_entity_abs_path("__meta__"), 'w') as f:
                    json.dump(meta, f)

    def __class_getitem__(cls, item):
        cls.__entity_type_init = item
        return super().__class_getitem__(item)

    def __get_entity_abs_path(self, entity_id: str) -> str:
        return os.path.join(self.__table_abs_path, entity_id) + ".json"

    def __get_semaphore(self, entity_id: str) -> Semaphore:
        if entity_id not in self.__semaphores:
            self.__semaphores[entity_id] = Semaphore(value=1)
        return self.__semaphores[entity_id]

    def __delete_semaphore(self, entity_id: str):
        if entity_id in self.__semaphores:
            del self.__semaphores[entity_id]

    async def add(self, entity_id: str, entity: Entity):
        if self.entity_type is None:
            return
        if entity_id in __system_files__:
            raise NameError('This name cannot be used')
        async with self.__get_semaphore(entity_id):
            with open(self.__get_entity_abs_path(entity_id), "w") as f:
                f.write(entity.json())

    async def query(self, entity_id: str) -> Entity | None:
        if self.entity_type is None:
            return
        async with self.__get_semaphore(entity_id):
            if not os.path.exists(self.__get_entity_abs_path(entity_id)) or entity_id in __system_files__:
                return None
            with open(self.__get_entity_abs_path(entity_id)) as f:
                try:
                    return self.entity_type.parse_raw(f.read())
                except pydantic.error_wrappers.ValidationError:
                    return None

    async def query_all(self) -> dict[str, Entity] | None:
        if self.entity_type is None:
            return
        all_entities = {}
        for entity_filename in os.listdir(self.__table_abs_path):
            entity_id, entity_extensions = entity_filename.split('.')
            if not entity_extensions == 'json' or entity_id in __system_files__:
                continue
            entity = await self.query(entity_id)
            if entity is not None:
                all_entities[entity_id] = await self.query(entity_id)

        return all_entities

    async def delete(self, entity_id: str) -> bool:
        if self.entity_type is None:
            return False
        async with self.__get_semaphore(entity_id):
            if not os.path.exists(self.__get_entity_abs_path(entity_id)) or entity_id in __system_files__:
                return False
            os.unlink(self.__get_entity_abs_path(entity_id))
            return True

    async def acquire_transaction(self, entity_id: str):
        await self.__get_semaphore(entity_id).acquire()

    async def release_transaction(self, entity_id: str):
        self.__get_semaphore(entity_id).release()

    def inner_table(self, inner_table_name: str, entity_type: Type[Entity] = None) -> 'ITable[Entity]':
        if inner_table_name not in self.__tables:
            self.__tables[inner_table_name] = Table[entity_type](inner_table_name, self.__table_abs_path)
        return self.__tables[inner_table_name]

    def get_inner_table(self, inner_table_name: str) -> Optional['ITable[Entity]']:
        if inner_table_name in self.__tables:
            return self.__tables[inner_table_name]

    def get_all_inner_tables(self) -> Optional[dict[str, 'ITable[Entity]']]:
        all_inner_tables = {}

        for inner_table_filename in os.listdir(self.__table_abs_path):
            pass
            # entity_id, entity_extensions = entity_filename.split('.')
            # if not entity_extensions == 'json' or entity_id in __system_files__:
            #     continue
            # all_entities[entity_id] = await self.query(entity_id)

        return all_inner_tables

    def delete_inner_table(self, inner_table_name: str) -> bool:
        if inner_table_name in self.__tables:
            del self.__tables[inner_table_name]
        table_path = os.path.join(self.__table_abs_path, inner_table_name)
        if os.path.exists(table_path):
            os.rmdir(table_path)
            return True
        return False
