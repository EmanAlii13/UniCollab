import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from pymongo import MongoClient
from app.services.project_service import ProjectService

# =========================
# تحميل متغيرات البيئة
# =========================
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "project_db")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI is not set in environment variables")

# =========================
# MongoDB Client (DEV MODE)
# =========================
mongo_client = MongoClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True,  # فقط للتطوير
    serverSelectionTimeoutMS=5000
)

# =========================
# Service Layer
# =========================
service = ProjectService(
    mongo_uri=MONGO_URI,
    db_name=DB_NAME
)

# =========================
# FastAPI App
# =========================
app = FastAPI(
    title="Project Service API",
    version="1.0.0",
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Local Docker"
        }
    ]
)

# =========================
# CORS (DEV)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8000",
        "http://127.0.0.1",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Schemas
# =========================
class ProjectCreate(BaseModel):
    title: str
    description: str
    leader: str

class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

class AddMember(BaseModel):
    username: str

# =========================
# Routes
# =========================
@app.get("/")
def root():
    return {"message": "Project Service is running. Visit /docs"}

@app.post("/api/v1/projects")
def create_project(project: ProjectCreate):
    try:
        project_id = service.create_project(
            project.title,
            project.description,
            project.leader
        )
        return {"project_id": project_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/projects")
def get_all_projects():
    try:
        return service.get_all_projects()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/projects/{project_id}")
def get_project(project_id: str):
    try:
        project = service.get_project(project_id)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/api/v1/projects/{project_id}")
def update_project(project_id: str, update: ProjectUpdate):
    try:
        updated = service.update_project(
            project_id,
            update.title,
            update.description
        )
        if not updated:
            raise HTTPException(status_code=404, detail="Project not found")
        return {"message": "Updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/projects/{project_id}/members")
def add_member(project_id: str, member: AddMember):
    try:
        added = service.add_member(project_id, member.username)
        if not added:
            raise HTTPException(
                status_code=400,
                detail="Cannot add member (limit reached or project not found)"
            )
        return {"message": "Member added"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
