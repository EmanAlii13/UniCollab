# UniCollab - CLI - project_client.py
import requests

PROJECT_SERVICE_URL = "http://localhost:8000"  # Localhost for Project Service

# =========================
# Create a new project
# =========================
def create_project(title, desc, leader):
    resp = requests.post(
        f"{PROJECT_SERVICE_URL}/api/v1/projects/projects",
        json={"title": title, "description": desc, "leader": leader}
    )
    resp.raise_for_status()
    return resp.json()["project_id"]

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
    return resp.json()

# =========================
# Update project
# =========================
def update_project(project_id, title=None, desc=None):
    data = {}
    if title:
        data["title"] = title
    if desc:
        data["description"] = desc
    resp = requests.put(
        f"{PROJECT_SERVICE_URL}/api/v1/projects/projects/{project_id}",
        json=data
    )
    resp.raise_for_status()
    return resp.json()["project"]

# =========================
# Add member to project (تصحيح)
# =========================
def add_member(project_id, member_email):
    resp = requests.post(
        f"{PROJECT_SERVICE_URL}/api/v1/projects/projects/{project_id}/members",
        params={"member_name": member_email}  # ✅ إرسال member_name كـquery parameter
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
