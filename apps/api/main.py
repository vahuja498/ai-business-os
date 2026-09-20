from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.api.config import settings
from apps.api.routers import (
    agents,
    approvals,
    audit,
    businesses,
    dashboard,
    health,
    opportunities,
    tasks,
)
from database.connection import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    await init_db()
    yield


app = FastAPI(
    title="AI Business OS API",
    description="Reusable autonomous-business operating system API",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health.router)
app.include_router(dashboard.router)
app.include_router(businesses.router)
app.include_router(opportunities.router)
app.include_router(approvals.router)
app.include_router(agents.router)
app.include_router(tasks.router)
app.include_router(audit.router)


@app.get("/")
async def root():
    return {
        "system": "AI Business OS",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health",
        "dashboard_summary": "/dashboard/summary",
    }
