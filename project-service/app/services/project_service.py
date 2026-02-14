# UniCollab - service - project_service.py
import uuid

from app.storage.storage_interface import RealStorage


class ProjectService:
    def __init__(self, storage: RealStorage):
        self.storage = storage
        self.data = self.storage.load()  # يجيب المشاريع من MongoDB مباشرة

    def create_project(self, title: str, desc: str, leader: str):
        project_id = str(uuid.uuid4())
        self.data["projects"][project_id] = {
            "title": title,
            "desc": desc,
            "leader": leader,
            "members": [],
        }
        self.storage.save(self.data)
        return project_id

    def get_project(self, project_id: str):
        return self.data["projects"].get(project_id)

    def get_all_projects(self):
        return self.data["projects"]

    def update_project(self, project_id: str, title: str = None, desc: str = None):
        project = self.data["projects"].get(project_id)
        if not project:
            return None
        if title:
            project["title"] = title
        if desc:
            project["desc"] = desc
        self.storage.save(self.data)
        return project

    def remove_project(self, project_id: str):
        if project_id in self.data["projects"]:
            del self.data["projects"][project_id]
            self.storage.save(self.data)
            return True
        return False

    def add_member(self, project_id: str, member_name: str):
        project = self.data["projects"].get(project_id)
        if not project:
            return False
        if member_name not in project["members"]:
            project["members"].append(member_name)
            self.storage.save(self.data)
        return True
