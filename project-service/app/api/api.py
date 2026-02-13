from fastapi import FastAPI
from app.api.v1 import project_endpoints

app = FastAPI(
    title="UniCollab Project Service",
    description="REST API with OpenAPI, JWT, SOLID, Design Patterns",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(project_endpoints.router, prefix="/api/v1/projects")
