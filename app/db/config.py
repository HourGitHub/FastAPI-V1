# app/db/config.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine and session
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

# Session local for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class separately without importing models
Base = declarative_base()

# Dependency to get DB session for routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize the database and create tables
def init_db():
    # Import models here to avoid circular imports
    from app.db.models import User, OTP, Role, Gender  # Import all relevant models
    Base.metadata.create_all(bind=engine) 
