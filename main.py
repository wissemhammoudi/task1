from fastapi import FastAPI 
import uvicorn  
from database import  engine
import models 
import routers.question,routers.choices,routers.test

# Create database tables based on SQLAlchemy models
models.Base.metadata.create_all(bind=engine)
# Create FastAPI application instance
app = FastAPI()
# Include routers for questions and choices endpoints
app.include_router(routers.question.router)
app.include_router(routers.choices.router)
app.include_router(routers.test.router)



# Root endpoint that returns a welcome message
@app.get("/")
async def root():
    return {"message": "hello "}

