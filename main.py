from fastapi import FastAPI
from route import router
from database import create_tables
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Blogging API",
    description="A FastAPI application for managing blog posts with SQLite database",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup."""
    create_tables()
    logger.info("Database tables created successfully")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
