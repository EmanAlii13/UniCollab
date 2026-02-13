from app.services.project_service import ProjectService
from app.storage.storage_interface import RealStorage
from fastapi import APIRouter, HTTPException

router = APIRouter()
storage = RealStorage()
service = ProjectService(storage)


@router.post("/projects")
def create_project(title: str, desc: str, leader: str):
    project_id = service.create_project(title, desc, leader)
    return {"project_id": project_id, "message": "Project created successfully"}


@router.get("/projects/{project_id}")
def get_project(project_id: str):
    project = service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/projects")
def get_all_projects():
    return service.get_all_projects()


@router.put("/projects/{project_id}")
def update_project(project_id: str, title: str = None, desc: str = None):
    updated = service.update_project(project_id, title, desc)
    if updated is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project updated successfully", "project": updated}


@router.delete("/projects/{project_id}")
def remove_project(project_id: str):
    removed = service.remove_project(project_id)
    if not removed:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project removed successfully"}


@router.post("/projects/{project_id}/members")
def add_member(project_id: str, member_name: str):
    success = service.add_member(project_id, member_name)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": f"Member {member_name} added successfully"}
