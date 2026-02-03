from app.services.project_service import ProjectService
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Project Service API",
    version="1.0.0",
    description="API for managing projects and teams",
)

service = ProjectService()

# ---------- Schemas ----------


class ProjectCreate(BaseModel):
    title: str
    description: str
    leader: str


class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class AddMember(BaseModel):
    username: str


# ---------- Endpoints ----------


@app.post("/api/v1/projects")
def create_project(project: ProjectCreate):
    project_id = service.create_project(
        project.title, project.description, project.leader
    )
    return {"project_id": project_id, "message": "Project created successfully"}


@app.get("/api/v1/projects")
def get_all_projects():
    return service.data["projects"]


@app.get("/api/v1/projects/{project_id}")
def get_project(project_id: str):
    project = service.data["projects"].get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.put("/api/v1/projects/{project_id}")
def update_project(project_id: str, update: ProjectUpdate):
    project = service.data["projects"].get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    if update.title:
        project["title"] = update.title
    if update.description:
        project["desc"] = update.description

    service.save_data()
    return {"message": "Project updated successfully"}


@app.post("/api/v1/projects/{project_id}/members")
def add_member(project_id: str, member: AddMember):
    project = service.data["projects"].get(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project["members"].append(member.username)
    service.save_data()
    return {"message": "Member added successfully"}
