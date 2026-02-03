import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "unicollab"
COLLECTION_NAME = "projects"


class MongoStorage:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def load(self):
        """جلب كل المشاريع من المونجو"""
        projects = {}
        for doc in self.collection.find({}):
            project_id = str(doc["_id"])
            projects[project_id] = {
                "title": doc["title"],
                "desc": doc["desc"],
                "leader": doc["leader"],
                "members": doc["members"],
            }
        return {"projects": projects}

    def save(self, data):
        """حفظ المشاريع إلى المونجو"""
        for project_id, project in data["projects"].items():
            self.collection.update_one(
                {"_id": project_id},
                {
                    "$set": {
                        "title": project["title"],
                        "desc": project["desc"],
                        "leader": project["leader"],
                        "members": project["members"],
                    }
                },
                upsert=True,
            )
