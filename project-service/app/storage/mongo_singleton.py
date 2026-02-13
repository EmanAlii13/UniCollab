from pymongo import MongoClient


class MongoClientSingleton:
    _instance = None

    @classmethod
    def get_client(cls, mongo_uri):
        if cls._instance is None:
            cls._instance = MongoClient(mongo_uri)
        return cls._instance
