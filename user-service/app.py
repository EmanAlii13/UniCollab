# user-service/app.py
from fastapi import FastAPI
from routes.auth import router as auth_router

app = FastAPI(
    title="UniCollab User Service",
    description="User management microservice for UniCollab project system",
    version="1.0.0"
)

# =========================
# Health Check Endpoint
# =========================
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# =========================
# Include routers
# =========================
app.include_router(auth_router)
