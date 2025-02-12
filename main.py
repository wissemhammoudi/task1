from fastapi import FastAPI 
import uvicorn  
from database import  engine
import models 
import routers.question,routers.choices,routers.test,routers.user
from models import metadata
import routers.user
# Create database tables based on SQLAlchemy models
metadata.create_all(engine)

# Create FastAPI application instance
app = FastAPI()
# Include routers for questions and choices endpoints
"""app.include_router(routers.question.router)
app.include_router(routers.choices.router)
app.include_router(routers.test.router)"""
app.include_router(routers.user.router)


# Root endpoint that returns a welcome message
@app.get("/")
async def root():
    return {"message": "hello "}

