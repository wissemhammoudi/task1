from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import  Depends
from dotenv import load_dotenv
import os

vd
load_dotenv()
# Database URL for PostgreSQL connection
# Format: postgresql://<username>:<password>@<host>:<port>/<database_name>
DATABASE_URL = os.getenv('DATABASE_URL')

# Create SQLAlchemy engine instance to manage database connections
engine = create_engine(DATABASE_URL)

# Create SessionLocal class to handle database sessions
# autocommit=False: Changes must be explicitly committed
# autoflush=False: Changes won't be automatically flushed to DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
# Used as parent class for all SQLAlchemy models
Base = declarative_base()

# Database dependency function
def get_db():
    """
    Generator function that manages database session lifecycle
    Yields a database session and ensures it's closed after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Type annotated database dependency for FastAPI
# Used to inject database sessions into route handlers
db_dependency = Annotated[Session, Depends(get_db)]