from sqlalchemy import create_engine,URL
from typing import Annotated
from fastapi import  Depends
from dotenv import load_dotenv
from sqlalchemy.engine import Connection
import os

load_dotenv()
# Database URL for PostgreSQL connection
# Format: postgresql://<username>:<password>@<host>:<port>/<database_name>
DATABASE_URL = os.getenv('DATABASE_URL')
DATABASE_NAME = os.getenv('DATABASE_NAME')
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
DATABASE = os.getenv('DATABASE')
url = URL.create(
    drivername="postgresql+psycopg2",
    username="admin",
    password="admin",
    host="postgres",
    port=5432,
    database="quizapplication"
)

# Create SQLAlchemy engine instance to manage database connections
engine = create_engine(url)

def get_db_core():
    connection = engine.connect()
    try:
        yield connection
    finally:
        connection.close()

# Type annotated database dependency for FastAPI
# Used to inject database sessions into route handlers
db_dependency_core=Annotated[Connection,Depends(get_db_core)]