from __future__ import annotations

from pymongo import MongoClient

from server import settings

client = MongoClient(settings.MONGO_HOST)
db = client['mycloud']

collection = db['registration_queue']
collection.create_index('expirationTime', expireAfterSeconds=0)
