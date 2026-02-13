import uuid

class Project:
    def __init__(self, title, description, leader_id, project_id=None):
        self.project_id = project_id or str(uuid.uuid4())
        self.title = title
        self.description = description
        self.leader_id = leader_id
        self.team_ids = [leader_id]
        self.join_requests = []

    def to_dict(self):
        return {
            "_id": self.project_id,
            "title": self.title,
            "desc": self.description,
            "leader": self.leader_id,
            "members": self.team_ids,
            "pending_requests": self.join_requests,
        }

    @staticmethod
    def from_dict(data):
        project = Project(
            title=data["title"],
            description=data["desc"],
            leader_id=data["leader"],
            project_id=data["_id"],
        )
        project.team_ids = data.get("members", [])
        project.join_requests = data.get("pending_requests", [])
        return project
