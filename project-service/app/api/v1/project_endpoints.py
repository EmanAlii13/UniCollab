# UniCollab - project-service - project_endpoints.py
from typing import Optional

from app.services.project_service import ProjectService
from app.storage.storage_interface import RealStorage
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

storage = RealStorage()
service = ProjectService(storage)


# =========================
# Request Models
# =========================


class ProjectCreate(BaseModel):
    title: str
    description: str
    leader: str


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class AddMemberRequest(BaseModel):
    username: str


# =========================
# Endpoints
# =========================


@router.post("/")
def create_project(project: ProjectCreate):
    project_id = service.create_project(
        project.title, project.description, project.leader
    )
    return {"project_id": project_id, "message": "Project created successfully"}


@router.get("/")
def get_all_projects():
    return service.get_all_projects()


@router.get("/{project_id}")
def get_project(project_id: str):
    project = service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}")
def update_project(project_id: str, project: ProjectUpdate):
    updated = service.update_project(project_id, project.title, project.description)
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project updated successfully", "project": updated}


@router.delete("/{project_id}")
def delete_project(project_id: str):
    removed = service.remove_project(project_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project removed successfully"}


@router.post("/{project_id}/members")
def add_member(project_id: str, data: AddMemberRequest):
    success = service.add_member(project_id, data.username)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": f"Member {data.username} added successfully"}
