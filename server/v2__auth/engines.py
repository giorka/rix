from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from pymongo.collection import Collection


class BaseStackEngine(ABC):
    @abstractmethod
    def push(self, document: dict) -> dict:
        raise NotImplementedError()

    @abstractmethod
    def find(self, document: dict) -> dict | None:
        raise NotImplementedError()

    @abstractmethod
    def pop(self, _id: int) -> int:
        raise NotImplementedError()

    @abstractmethod
    def flush(self) -> None:
        raise NotImplementedError()


@dataclass
class MongoDBStackEngine(BaseStackEngine):
    collection: Collection

    def push(self, document: dict) -> dict:
        self.collection.insert_one(document=document)

        return document

    def find(self, document: dict) -> dict | None:
        return self.collection.find_one(document)

    def pop(self, _id: int) -> int:
        self.collection.delete_one({'_id': _id})

        return _id

    def flush(self) -> None:
        self.collection.delete_many({})
