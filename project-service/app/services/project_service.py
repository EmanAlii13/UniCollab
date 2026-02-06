from .mongo_storage import MongoStorage


class ProjectService:
    def __init__(self, storage=None):
        if storage is None:
            self.storage = MongoStorage()
        else:
            self.storage = storage

        try:
            self.data = self.storage.load()
        except Exception:
            self.data = {"projects": {}}

        if "projects" not in self.data or not isinstance(self.data["projects"], dict):
            self.data["projects"] = {}

    def save_data(self):
        self.storage.save(self.data)

    def create_project(self, title, desc, leader):
        project_id = str(len(self.data["projects"]) + 1)
        self.data["projects"][project_id] = {
            "title": title,
            "desc": desc,
            "leader": leader,
            "members": [],
        }
        self.save_data()
        return project_id

    def join_project(self, project_id, member):
        if project_id in self.data["projects"]:
            self.data["projects"][project_id]["members"].append(member)
            self.save_data()
            return True
        return False
