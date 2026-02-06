class ProjectService:
    def __init__(self, storage):
        self.storage = storage

        try:
            self.data = self.storage.load()
        except Exception:
            self.data = {"projects": {}}

        if "projects" not in self.data or not isinstance(self.data["projects"], dict):
            self.data["projects"] = {}

    def save_data(self):
        self.storage.save(self.data)

    # -----------------------------
    # CREATE PROJECT
    # -----------------------------
    def create_project(self, title, desc, leader):
        project_id = str(len(self.data["projects"]) + 1)

        self.data["projects"][project_id] = {
            "title": title,
            "desc": desc,
            "leader": leader,
            "members": [leader],  # القائد عضو تلقائياً
            "pending_requests": [],  # طلبات الانضمام
        }

        self.save_data()
        return project_id

    # -----------------------------
    # JOIN PROJECT (REQUEST)
    # -----------------------------
    def join_project(self, project_id, user_id):
        project = self.data["projects"].get(project_id)
        if not project:
            return False

        if user_id in project["members"]:
            return False

        if user_id not in project["pending_requests"]:
            project["pending_requests"].append(user_id)
            self.save_data()

        return True

    # -----------------------------
    # APPROVE REQUEST
    # -----------------------------
    def approve_request(self, project_id, user_id):
        project = self.data["projects"].get(project_id)
        if not project:
            return False

        if user_id in project["pending_requests"]:
            project["pending_requests"].remove(user_id)
            project["members"].append(user_id)
            self.save_data()
            return True

        return False
