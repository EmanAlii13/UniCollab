from abc import ABC, abstractmethod
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env
load_dotenv()  

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "unicollab")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "projects")

class StorageInterface(ABC):
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self, data):
        pass

class RealStorage(StorageInterface):
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def load(self):
        projects = {}
        for doc in self.collection.find():
            projects[str(doc["_id"])] = {
                "title": doc["title"],
                "desc": doc["desc"],
                "leader": doc["leader"],
                "members": doc.get("members", [])
            }
        return {"projects": projects}

    def save(self, data):
        for project_id, project in data["projects"].items():
            self.collection.update_one(
                {"_id": project_id},
                {"$set": {
                    "title": project["title"],
                    "desc": project["desc"],
                    "leader": project["leader"],
                    "members": project.get("members", [])
                }},
                upsert=True
            )
