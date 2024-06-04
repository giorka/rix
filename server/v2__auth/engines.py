from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass

from pymongo.collection import Collection


class BaseStackEngine(ABC):
    @classmethod
    @abstractmethod
    def push(cls, document: dict) -> dict: ...

    @classmethod
    @abstractmethod
    def contains(cls, document: dict) -> bool: ...


@dataclass
class MongoDBStackEngine(BaseStackEngine):
    collection: Collection

    def push(self, document: dict) -> dict:
        self.collection.insert_one(document=document)

        return document

    def find(self, document: dict) -> dict | None:
        return self.collection.find_one(document)

    def contains(self, document: dict) -> bool:
        return bool(self.find(document=document))

    def pop(self, _id: int) -> int:
        self.collection.delete_one({'_id': _id})

        return _id
