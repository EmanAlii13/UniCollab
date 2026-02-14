from fastapi import FastAPI
from app.api.v1.project_endpoints import router as project_router

app = FastAPI(
    title="UniCollab Project Service",
    description="Project microservice with REST, OpenAPI, SOLID and Design Patterns",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(
    project_router,
    prefix="/api/v1/projects",
    tags=["Projects"]
)
