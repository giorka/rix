from __future__ import annotations

from pymongo import MongoClient

from server import settings

client = MongoClient(settings.MONGO_HOST)
db = client['mycloud']

verification_queue = db['verification_queue']
verification_queue.create_index('expirationTime', expireAfterSeconds=0)

revert_queue = db['revert_queue']
revert_queue.create_index('expirationTime', expireAfterSeconds=0)
