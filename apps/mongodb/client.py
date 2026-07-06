from pymongo import MongoClient

from django.conf import settings

client = MongoClient(
    host=settings.MONGO_HOST,
    port=settings.MONGO_PORT,
)

db = client[settings.MONGO_DB]