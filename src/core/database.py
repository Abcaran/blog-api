"""
Database configuration and session management for SQLite with SQLAlchemy.
"""
import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database configuration
DATABASE_URL = "sqlite:///./blog.db"

# Ensure the database directory exists
def ensure_db_directory():
    """Ensure the database directory exists."""
    db_path = Path("blog.db")
    db_dir = db_path.parent
    db_dir.mkdir(exist_ok=True)

ensure_db_directory()

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=False  # Set to True for SQL query logging
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency to get database session.
    This will be used with FastAPI's Depends.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Create all database tables.
    This should be called when the application starts.
    """
    Base.metadata.create_all(bind=engine)


def drop_tables():
    """
    Drop all database tables.
    Useful for testing or resetting the database.
    """
    Base.metadata.drop_all(bind=engine)


def reset_database():
    """
    Reset the database by dropping and recreating all tables.
    """
    drop_tables()
    create_tables()
