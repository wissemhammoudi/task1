from sqlalchemy import Column, Integer, String, ForeignKey,Boolean,MetaData,Table
from pydantic import BaseModel,Field ,EmailStr
from typing import Optional

metadata=MetaData()
"""
# Pydantic model for choice data validation
class ChoiceBase(BaseModel): # najmou nektbou interface 
    choice_text: str  # Text content of the choice
    is_correct: bool  # Boolean indicating if this is the correct answer

# Pydantic model for question data validation
class QuestionBase(BaseModel):
    question_text: str  # Text content of the question
    choices: List[ChoiceBase]  # List of associated choices
# SQLAlchemy model for questions table
class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True)  # Primary key column
    question_text = Column(String, index=True)  # Question text content

# SQLAlchemy model for choices table 
class Choice(Base):
    __tablename__ = "choices"
    id = Column(Integer, primary_key=True)  # Primary key column
    choice_text = Column(String, index=True)  # Choice text content
    is_correct = Column(Boolean, default=False)  # Indicates if choice is correct
    question_id = Column(Integer, ForeignKey("questions.id"))  # Foreign key to questions table
"""
# Pydantic model for Location
class LocationBase(BaseModel):
    address: str = Field(..., max_length=255)
    city: str = Field(..., max_length=100)

# Pydantic model for Person
class PersonBase(BaseModel):
    username: str = Field(..., max_length=15)
    email_address: EmailStr = Field(..., max_length=255)
    location_id: Optional[LocationBase] = None  # Location ID will be optional for person creation



# SQLAlchemy table for Person with location_id (ForeignKey to location_table)
person_table = Table(
    "person", metadata,
    Column("person_id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(15), nullable=False, unique=True),
    Column("email_address", String(255), nullable=False),
    Column("location_id", Integer, ForeignKey('location.location_id'), nullable=True)  
)

# SQLAlchemy table for Location
location_table = Table(
    "location", metadata,
    Column("location_id", Integer, primary_key=True, autoincrement=True),
    Column("address", String(255), nullable=False),
    Column("city", String(100), nullable=False),
)


