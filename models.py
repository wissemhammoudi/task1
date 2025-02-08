from sqlalchemy import Column, Integer, String, ForeignKey,Boolean
from database import Base
from pydantic import BaseModel
from typing import List

# Pydantic model for choice data validation
class ChoiceBase(BaseModel):
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
