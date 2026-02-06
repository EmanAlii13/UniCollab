class Project:
    def __init__(self, title, description, leader_id):
        self.title = title
        self.description = description
        self.leader_id = leader_id
        self.team_ids = [leader_id]
        self.join_requests = []
