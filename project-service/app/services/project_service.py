from app.services.project_factory import ProjectFactory
from bson.objectid import ObjectId
from pymongo import MongoClient


class ProjectService:
    """
    Service layer لإدارة المشاريع.
    يدعم التخزين على MongoDB أو أي Storage يطبق واجهة load/save
    """

    def __init__(self, storage=None, mongo_uri=None, db_name="project_db"):
        # Dependency Injection → loose coupling + testability
        if mongo_uri:
            self.client = MongoClient(mongo_uri)
            self.db = self.client[db_name]
            self.projects = self.db["projects"]
        else:
            self.projects = None
            self.data = storage.load() if storage else {"projects": {}}
            self.storage = storage

    # -----------------------------
    # CREATE PROJECT
    # -----------------------------
    def create_project(self, title, desc, leader):
        project_data = ProjectFactory.create(title, desc, leader)
        if self.projects is not None:
            result = self.projects.insert_one(project_data)
            return str(result.inserted_id)
        else:
            project_id = str(len(self.data["projects"]) + 1)
            self.data["projects"][project_id] = project_data
            if self.storage:
                self.storage.save(self.data)
            return project_id

    # -----------------------------
    # GET ALL PROJECTS
    # -----------------------------
    def get_all_projects(self):
        if self.projects is not None:
            projects = list(self.projects.find())
            for p in projects:
                p["_id"] = str(p["_id"])
            return {p["_id"]: p for p in projects}
        else:
            return self.data["projects"]

    # -----------------------------
    # GET SINGLE PROJECT
    # -----------------------------
    def get_project(self, project_id):
        if self.projects is not None:
            project = self.projects.find_one({"_id": ObjectId(project_id)})
            if project:
                project["_id"] = str(project["_id"])
            return project
        else:
            return self.data["projects"].get(project_id)

    # -----------------------------
    # UPDATE PROJECT
    # -----------------------------
    def update_project(self, project_id, title=None, desc=None):
        if self.projects is not None:
            update_data = {}
            if title:
                update_data["title"] = title
            if desc:
                update_data["desc"] = desc
            if update_data:
                result = self.projects.update_one(
                    {"_id": ObjectId(project_id)}, {"$set": update_data}
                )
                return result.modified_count > 0
            return False
        else:
            project = self.data["projects"].get(project_id)
            if not project:
                return False
            if title:
                project["title"] = title
            if desc:
                project["desc"] = desc
            if self.storage:
                self.storage.save(self.data)
            return True

    # -----------------------------
    # ADD MEMBER
    # -----------------------------
    def add_member(self, project_id, username):
        project = self.get_project(project_id)
        if not project:
            return False
        if username in project.get("members", []):
            return True
        if len(project["members"]) >= 3:
            return False

        if self.projects is not None:
            self.projects.update_one(
                {"_id": ObjectId(project_id)}, {"$push": {"members": username}}
            )
        else:
            project["members"].append(username)
            if self.storage:
                self.storage.save(self.data)
        return True

    # -----------------------------
    # JOIN PROJECT REQUEST
    # -----------------------------
    def join_project(self, project_id, user_id):
        project = self.get_project(project_id)
        if not project or user_id in project.get("members", []):
            return False
        if user_id not in project.get("pending_requests", []):
            if self.projects is not None:
                self.projects.update_one(
                    {"_id": ObjectId(project_id)},
                    {"$push": {"pending_requests": user_id}},
                )
            else:
                project.setdefault("pending_requests", []).append(user_id)
                if self.storage:
                    self.storage.save(self.data)
        return True

    # -----------------------------
    # APPROVE REQUEST
    # -----------------------------
    def approve_request(self, project_id, user_id):
        project = self.get_project(project_id)
        if not project or user_id not in project.get("pending_requests", []):
            return False

        if self.projects is not None:
            self.projects.update_one(
                {"_id": ObjectId(project_id)},
                {
                    "$pull": {"pending_requests": user_id},
                    "$push": {"members": user_id},
                },
            )
        else:
            project["pending_requests"].remove(user_id)
            project["members"].append(user_id)
            if self.storage:
                self.storage.save(self.data)
        return True
