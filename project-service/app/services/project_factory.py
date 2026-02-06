import uuid


class ProjectFactory:
    @staticmethod
    def create(title, desc, leader):
        return {
            "_id": str(uuid.uuid4()),
            "title": title,
            "desc": desc,
            "leader": leader,
            "members": [leader],
            "join_requests": [],
        }
