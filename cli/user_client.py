# UniCollab - CLI - user_client.py
import requests

USER_SERVICE_URL = "http://localhost:8001"  # Localhost for User Service

def login(email, password):
    resp = requests.post(f"{USER_SERVICE_URL}/login", json={"email": email, "password": password})
    resp.raise_for_status()
    return resp.json()

def logout(email):
    resp = requests.post(f"{USER_SERVICE_URL}/logout", json={"email": email})
    resp.raise_for_status()
    return resp.json()

def get_me(email):
    resp = requests.get(f"{USER_SERVICE_URL}/me", params={"email": email})
    resp.raise_for_status()
    return resp.json()

def can_join_project(email):
    resp = requests.get(f"{USER_SERVICE_URL}/users/{email}/status")
    resp.raise_for_status()
    return resp.json().get("can_join_project", False)

def assign_project(email, project_id, role):
    resp = requests.post(f"{USER_SERVICE_URL}/users/{email}/assign-project", json={"project_id": project_id, "role": role})
    resp.raise_for_status()
    return resp.json()

def remove_project(email):
    resp = requests.post(f"{USER_SERVICE_URL}/users/{email}/remove-project")
    resp.raise_for_status()
    return resp.json()
