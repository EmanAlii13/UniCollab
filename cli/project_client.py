# UniCollab - CLI - project_client.py
import requests

PROJECT_SERVICE_URL = "http://localhost:8000"  # Localhost for Project Service

# =========================
# Create a new project
# =========================
def create_project(title, desc, leader):
    resp = requests.post(
        f"{PROJECT_SERVICE_URL}/api/v1/projects/projects",
        params={"title": title, "desc": desc, "leader": leader}  # ⚡ استخدام params بدل json
    )
    resp.raise_for_status()
    return resp.json()["project_id"]  # ⚡ استخدم project_id مباشرة

# =========================
# Get project by ID
# =========================
def get_project(project_id):
    resp = requests.get(f"{PROJECT_SERVICE_URL}/api/v1/projects/projects/{project_id}")
    resp.raise_for_status()
    return resp.json()

# =========================
# Get all projects
# =========================
def get_all_projects():
    resp = requests.get(f"{PROJECT_SERVICE_URL}/api/v1/projects/projects")
    resp.raise_for_status()
    return resp.json()  # ⚡ بيرجع dict {project_id: project_data}

# =========================
# Update project
# =========================
def update_project(project_id, title=None, desc=None):
    resp = requests.put(
        f"{PROJECT_SERVICE_URL}/api/v1/projects/projects/{project_id}",
        params={"title": title, "desc": desc}
    )
    resp.raise_for_status()
    return resp.json()["project"]  # ⚡ استخدم المشروع من المفتاح 'project'

# =========================
# Add member to project
# =========================
def add_member(project_id, member_email):
    resp = requests.post(
        f"{PROJECT_SERVICE_URL}/api/v1/projects/projects/{project_id}/members",
        json={"member_name": member_email}
    )
    resp.raise_for_status()
    return resp.json()["message"]

# =========================
# Remove / delete project by ID
# =========================
def remove_project_by_id(project_id):
    resp = requests.delete(f"{PROJECT_SERVICE_URL}/api/v1/projects/projects/{project_id}")
    resp.raise_for_status()
    return resp.json()["message"]
