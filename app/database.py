import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Ensure DATABASE_URL is loaded correctly
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL or DATABASE_URL == "127.0.0.1":
    raise ValueError("DATABASE_URL is not set properly. Check your .env file!")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model for SQLAlchemy
Base = declarative_base()

# Add this function for database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()