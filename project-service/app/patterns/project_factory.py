# from app.model.project import Project  ← علقه مؤقتًا
import uuid

# from app.models.project import Project


class ProjectFactory:
    @staticmethod
    def create(title, desc, leader):
        return {
            "_id": str(uuid.uuid4()),
            "title": title,
            "desc": desc,
            "leader": leader,
            "members": [leader],
            "pending_requests": [],
        }
