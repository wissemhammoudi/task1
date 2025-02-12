from fastapi import FastAPI 
import uvicorn  
from database import  engine
import routers.question,routers.choices,routers.test,routers.user,routers.userORM
from models import metadata
from modelORM import Base
import routers.user
import routers.userORM
# Create database tables based on SQLAlchemy models
#metadata.create_all(engine)
Base.metadata.create_all(engine)
# Create FastAPI application instance
app = FastAPI()
# Include routers for questions and choices endpoints
"""app.include_router(routers.question.router)
app.include_router(routers.choices.router)
app.include_router(routers.test.router)"""
app.include_router(routers.user.router)
app.include_router(routers.userORM.router)

# Root endpoint that returns a welcome message
@app.get("/")
async def root():
    return {"message": "hello "}

