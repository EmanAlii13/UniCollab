from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services.project_service import ProjectService
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "project_db")

app = FastAPI(title="Project Service API", version="1.0.0")

service = ProjectService(mongo_uri=MONGO_URI, db_name=DB_NAME)

# Schemas
class ProjectCreate(BaseModel):
    title: str
    description: str
    leader: str

class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

class AddMember(BaseModel):
    username: str

# Routes
@app.get("/")
def root():
    return {"message": "Welcome! Visit /docs for API docs"}

@app.post("/api/v1/projects")
def create_project(project: ProjectCreate):
    try:
        project_id = service.create_project(project.title, project.description, project.leader)
        return {"project_id": project_id, "message": "Project created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating project: {e}")

@app.get("/api/v1/projects")
def get_all_projects():
    try:
        projects = service.get_all_projects()
        return projects if projects else {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching projects: {e}")

@app.get("/api/v1/projects/{project_id}")
def get_project(project_id: str):
    try:
        project = service.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching project: {e}")

@app.put("/api/v1/projects/{project_id}")
def update_project(project_id: str, update: ProjectUpdate):
    try:
        updated = service.update_project(project_id, update.title, update.description)
        if not updated:
            raise HTTPException(status_code=404, detail="Project not found")
        return {"message": "Project updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating project: {e}")

@app.post("/api/v1/projects/{project_id}/members")
def add_member(project_id: str, member: AddMember):
    try:
        added = service.add_member(project_id, member.username)
        if not added:
            raise HTTPException(status_code=400, detail="Cannot add member (max 3 or project not found)")
        return {"message": "Member added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding member: {e}")
