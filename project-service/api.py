from app.services.project_service import ProjectService  # <-- import صحيح
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# ----------------- FastAPI App -----------------
app = FastAPI(
    title="Project Service API",
    version="1.0.0",
    description="API for managing projects and teams",
)

# ----------------- MongoDB URI -----------------
MONGO_URI = "mongodb+srv://ayatsdr7_db_user:t5hxpUD44Cn0gXiZ@cluster0.zpmqytz.mongodb.net/?appName=Cluster0"

# ----------------- ProjectService -----------------
service = ProjectService(
    mongo_uri=MONGO_URI, db_name="testproject"
)  # <-- استخدم mongo_uri و db_name


# ----------------- Schemas -----------------
class ProjectCreate(BaseModel):
    title: str
    description: str
    leader: str


class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class AddMember(BaseModel):
    username: str


# ----------------- Routes -----------------
@app.get("/")
def root():
    return {"message": "Welcome! Visit /docs for API docs"}


@app.post("/api/v1/projects")
def create_project(project: ProjectCreate):
    project_id = service.create_project(
        project.title, project.description, project.leader
    )
    return {"project_id": project_id, "message": "Project created successfully"}


@app.get("/api/v1/projects")
def get_all_projects():
    return service.get_all_projects()


@app.get("/api/v1/projects/{project_id}")
def get_project(project_id: str):
    project = service.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.put("/api/v1/projects/{project_id}")
def update_project(project_id: str, update: ProjectUpdate):
    updated = service.update_project(project_id, update.title, update.description)
    if not updated:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project updated successfully"}


@app.post("/api/v1/projects/{project_id}/members")
def add_member(project_id: str, member: AddMember):
    added = service.add_member(project_id, member.username)
    if not added:
        raise HTTPException(
            status_code=400, detail="Cannot add member (max 3 or project not found)"
        )
    return {"message": "Member added successfully"}
