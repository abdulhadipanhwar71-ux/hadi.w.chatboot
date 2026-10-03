"""
WhatsApp Business Bot Application Entry Point.
All code and comments are strictly in English.
"""

import uvicorn
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import Base, engine
from app.seed import seed_sample_products
from app.routers import webhook, simulator, admin

BASE_DIR = Path(__file__).resolve().parent

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle event handler for database initialization and product seeding."""
    # Ensure database schema is created
    Base.metadata.create_all(bind=engine)
    # Seed initial products if catalog is empty
    seed_sample_products()
    yield

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Professional Multilingual WhatsApp Chatbot (Sindhi, Urdu, English) with Order Management and Admin Panel",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "app" / "static")), name="static")

# Include feature routers
app.include_router(webhook.router)
app.include_router(simulator.router)
app.include_router(admin.router)

@app.get("/", include_in_schema=False)
async def root_redirect():
    """Redirect home route to the Admin Dashboard."""
    return RedirectResponse(url="/admin")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
